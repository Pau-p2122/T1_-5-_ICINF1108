import pytest

from app.domain.exceptions.business_exceptions import BusinessException
from app.domain.services.auth_service import (
    AuthService,
    MAX_RECOVERY_REQUESTS,
    create_password_reset_jwt,
    verify_password,
)
from app.infrastructure.models.orm_models import ConsumedResetTokenModel


def test_integration_auth_status_endpoint(client):
    response = client.get("/api/v1/auth/")
    assert response.status_code == 200
    assert "activo" in response.json()["message"]


def test_integration_forgot_password_generic_response_existing_and_non_existing(
    client, sample_user
):
    res_existing = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": sample_user.email},
    )
    res_missing = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "desconocido@tcg.cl"},
    )

    assert res_existing.status_code == 200
    assert res_missing.status_code == 200
    assert res_existing.json() == res_missing.json()


def test_integration_forgot_password_rate_limit(client, sample_user):
    for _ in range(MAX_RECOVERY_REQUESTS):
        res = client.post(
            "/api/v1/auth/forgot-password",
            json={"email": sample_user.email},
        )
        assert res.status_code == 200

    blocked = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": sample_user.email},
    )
    assert blocked.status_code in (400, 429)
    assert "límite" in blocked.json()["error"]["message"].lower()


def test_integration_reset_password_updates_hash_and_token_version(
    client, db_session, sample_user
):
    token, payload = create_password_reset_jwt(
        user_id=sample_user.id,
        token_version=sample_user.token_version,
    )

    response = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token, "new_password": "NewStrongPass99"},
    )
    assert response.status_code == 200

    db_session.refresh(sample_user)
    assert verify_password("NewStrongPass99", sample_user.password_hash) is True
    assert verify_password("OldPass123", sample_user.password_hash) is False
    assert sample_user.token_version == 2
    assert sample_user.password_changed_at is not None

    consumed = (
        db_session.query(ConsumedResetTokenModel)
        .filter(ConsumedResetTokenModel.jti == payload["jti"])
        .first()
    )
    assert consumed is not None


def test_integration_reset_password_blocks_token_reuse(client, sample_user):
    token, _ = create_password_reset_jwt(
        user_id=sample_user.id,
        token_version=sample_user.token_version,
    )

    first = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token, "new_password": "NewStrongPass99"},
    )
    assert first.status_code == 200

    second = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token, "new_password": "AnotherPass99"},
    )
    assert second.status_code == 400
    assert "utilizado" in second.json()["error"]["message"].lower()


def test_integration_previous_recovery_tokens_invalidated_after_reset(
    client, sample_user
):
    token_a, _ = create_password_reset_jwt(
        user_id=sample_user.id,
        token_version=sample_user.token_version,
    )
    token_b, _ = create_password_reset_jwt(
        user_id=sample_user.id,
        token_version=sample_user.token_version,
    )

    res_a = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token_a, "new_password": "NewStrongPass99"},
    )
    assert res_a.status_code == 200

    res_b = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token_b, "new_password": "AnotherPass99"},
    )
    assert res_b.status_code == 400
    assert "invalidado" in res_b.json()["error"]["message"].lower()


def test_integration_token_cannot_modify_another_account(
    db_session, sample_user, second_user
):
    token_user_1, _ = create_password_reset_jwt(
        user_id=sample_user.id,
        token_version=sample_user.token_version,
    )
    service = AuthService(db=db_session)

    with pytest.raises(BusinessException) as exc:
        service.reset_password(
            token=token_user_1,
            new_password="HijackPass123",
            target_user_id=second_user.id,
        )
    assert "otra cuenta" in exc.value.message.lower()

    db_session.refresh(second_user)
    assert verify_password("RivalPass123", second_user.password_hash) is True
    assert second_user.token_version == 1