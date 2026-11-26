import base64
import hashlib
import hmac
import json
import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session

from app.domain.exceptions.business_exceptions import BusinessException
from app.infrastructure.models.orm_models import ConsumedResetTokenModel, UserModel

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-prod")
RESET_TOKEN_EXPIRE_MINUTES = 15
MAX_RECOVERY_REQUESTS = 3
RATE_LIMIT_WINDOW_SECONDS = 60

GENERIC_RECOVERY_MESSAGE = (
    "Si el correo está registrado, recibirás instrucciones para restablecer tu contraseña."
)


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("utf-8"))


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    iterations = 100_000
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        iterations,
    )
    return f"pbkdf2_sha256${iterations}${salt}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        scheme, iter_str, salt, expected_hex = stored_hash.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        iterations = int(iter_str)
        actual_digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
        )
        return hmac.compare_digest(actual_digest.hex(), expected_hex)
    except Exception:
        return False


def create_password_reset_jwt(
    user_id: int,
    token_version: int,
    expires_minutes: int = RESET_TOKEN_EXPIRE_MINUTES,
) -> Tuple[str, dict]:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "purpose": "password_reset",
        "token_version": token_version,
        "jti": str(uuid.uuid4()),
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    header = {"alg": "HS256", "typ": "JWT"}
    encoded_header = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    encoded_payload = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature = hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
    token = f"{encoded_header}.{encoded_payload}.{_b64url_encode(signature)}"
    return token, payload


def decode_password_reset_jwt(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise BusinessException("Token de recuperación inválido.")

    encoded_header, encoded_payload, encoded_sig = parts
    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    expected_sig = hmac.new(SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
    actual_sig = _b64url_decode(encoded_sig)

    if not hmac.compare_digest(expected_sig, actual_sig):
        raise BusinessException("Firma del token de recuperación inválida.")

    try:
        payload = json.loads(_b64url_decode(encoded_payload).decode("utf-8"))
    except Exception:
        raise BusinessException("Contenido del token inválido.")

    if payload.get("purpose") != "password_reset":
        raise BusinessException("El token no tiene permiso para restablecer contraseña.")

    exp = payload.get("exp")
    now_ts = int(datetime.now(timezone.utc).timestamp())
    if not isinstance(exp, int) or exp <= now_ts:
        raise BusinessException("El token de recuperación ha expirado.")

    if not payload.get("sub") or not payload.get("jti"):
        raise BusinessException("El token está incompleto.")

    return payload


class AuthService:
    def __init__(self, db: Session, request_history: Optional[Dict[str, List[float]]] = None):
        self.db = db
        self._request_history: Dict[str, List[float]] = (
            request_history if request_history is not None else {}
        )

    def _check_rate_limit(self, key: str) -> None:
        now_ts = datetime.now(timezone.utc).timestamp()
        recent = [
            ts
            for ts in self._request_history.get(key, [])
            if now_ts - ts < RATE_LIMIT_WINDOW_SECONDS
        ]
        if len(recent) >= MAX_RECOVERY_REQUESTS:
            raise BusinessException(
                "Has excedido el límite de solicitudes de recuperación. Intenta más tarde."
            )
        recent.append(now_ts)
        self._request_history[key] = recent

    def request_password_reset(self, email: str) -> dict:
        normalized_email = email.strip().lower()
        self._check_rate_limit(normalized_email)

        user = (
            self.db.query(UserModel)
            .filter(UserModel.email == normalized_email)
            .first()
        )
        reset_token: Optional[str] = None
        if user:
            reset_token, _ = create_password_reset_jwt(
                user_id=user.id,
                token_version=user.token_version,
            )

        return {
            "message": GENERIC_RECOVERY_MESSAGE,
            "reset_token": reset_token,
        }

    def reset_password(
        self, token: str, new_password: str, target_user_id: Optional[int] = None
    ) -> dict:
        payload = decode_password_reset_jwt(token)
        jti = payload["jti"]
        token_user_id = int(payload["sub"])
        token_version = payload.get("token_version")

        if target_user_id is not None and target_user_id != token_user_id:
            raise BusinessException("El token no autoriza modificar otra cuenta.")

        already_used = (
            self.db.query(ConsumedResetTokenModel)
            .filter(ConsumedResetTokenModel.jti == jti)
            .first()
        )
        if already_used:
            raise BusinessException("Este token de recuperación ya fue utilizado.")

        user = self.db.query(UserModel).filter(UserModel.id == token_user_id).first()
        if not user:
            raise BusinessException("Cuenta no válida para restablecer contraseña.")

        if token_version is not None and user.token_version != token_version:
            raise BusinessException(
                "El token ya fue invalidado por un cambio de contraseña anterior."
            )

        now = datetime.now(timezone.utc)
        expires_at = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)

        user.password_hash = hash_password(new_password)
        user.token_version += 1
        user.password_changed_at = now

        consumed = ConsumedResetTokenModel(
            jti=jti,
            user_id=user.id,
            expires_at=expires_at,
            used_at=now,
        )
        self.db.add(consumed)
        self.db.commit()
        self.db.refresh(user)

        return {
            "message": "Contraseña actualizada correctamente. Las sesiones y tokens anteriores fueron invalidados.",
            "user_id": user.id,
        }