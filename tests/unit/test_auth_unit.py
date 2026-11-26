import pytest
from pydantic import ValidationError

from app.application.schemas.auth_schemas import ResetPasswordRequest
from app.domain.exceptions.business_exceptions import BusinessException
from app.domain.services.auth_service import (
    AuthService,
    MAX_RECOVERY_REQUESTS,
    create_password_reset_jwt,
    decode_password_reset_jwt,
    hash_password,
    verify_password,
)


def test_unit_hash_and_verify_password():
    hashed = hash_password("SecretPass123")
    assert hashed.startswith("pbkdf2_sha256$")
    assert verify_password("SecretPass123", hashed) is True
    assert verify_password("WrongPass123", hashed) is False
    assert verify_password("SecretPass123", "invalid-format") is False


def test_unit_create_jwt_contains_purpose_exp_and_unique_jti():
    token1, payload1 = create_password_reset_jwt(user_id=10, token_version=1)
    token2, payload2 = create_password_reset_jwt(user_id=10, token_version=1)

    assert token1 != token2
    assert payload1["sub"] == "10"
    assert payload1["purpose"] == "password_reset"
    assert payload1["exp"] > payload1["iat"]
    assert payload1["jti"] != payload2["jti"]

    decoded = decode_password_reset_jwt(token1)
    assert decoded["jti"] == payload1["jti"]


def test_unit_decode_rejects_expired_token():
    token, _ = create_password_reset_jwt(user_id=1, token_version=1, expires_minutes=-1)
    with pytest.raises(BusinessException) as exc:
        decode_password_reset_jwt(token)
    assert "expirado" in exc.value.message.lower()


def test_unit_decode_rejects_tampered_signature():
    token, _ = create_password_reset_jwt(user_id=1, token_version=1)
    tampered = token[:-2] + ("ab" if not token.endswith("ab") else "cd")
    with pytest.raises(BusinessException) as exc:
        decode_password_reset_jwt(tampered)
    assert "firma" in exc.value.message.lower()


def test_unit_decode_rejects_malformed_token():
    with pytest.raises(BusinessException) as exc:
        decode_password_reset_jwt("not.a.valid.jwt.token")
    assert "inválido" in exc.value.message.lower()


def test_unit_dto_validates_password_complexity():
    with pytest.raises(ValidationError):
        ResetPasswordRequest(token="1234567890", new_password="weak")
    with pytest.raises(ValidationError):
        ResetPasswordRequest(token="1234567890", new_password="alllowercase1")
    with pytest.raises(ValidationError):
        ResetPasswordRequest(token="1234567890", new_password="ALLUPPERCASE1")
    with pytest.raises(ValidationError):
        ResetPasswordRequest(token="1234567890", new_password="NoNumbersHere")

    valid = ResetPasswordRequest(token="1234567890", new_password="ValidPass123")
    assert valid.new_password == "ValidPass123"


def test_unit_rate_limit_blocks_excess_requests(db_session):
    history = {}
    service = AuthService(db=db_session, request_history=history)

    for _ in range(MAX_RECOVERY_REQUESTS):
        res = service.request_password_reset("nobody@tcg.cl")
        assert "Si el correo está registrado" in res["message"]

    with pytest.raises(BusinessException) as exc:
        service.request_password_reset("nobody@tcg.cl")
    assert "límite" in exc.value.message.lower()