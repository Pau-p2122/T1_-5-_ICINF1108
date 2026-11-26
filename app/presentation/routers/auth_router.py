from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.application.schemas.auth_schemas import (
    ForgotPasswordRequest,
    MessageResponse,
    ResetPasswordRequest,
)
from app.domain.services.auth_service import AuthService
from app.infrastructure.database import get_db

router = APIRouter()
_shared_rate_limit_store: dict = {}


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db=db, request_history=_shared_rate_limit_store)


@router.get("/")
def auth_status():
    return {"message": "Módulo de autenticación y usuarios activo"}


@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
def forgot_password(
    payload: ForgotPasswordRequest,
    service: AuthService = Depends(get_auth_service),
):
    result = service.request_password_reset(payload.email)
    return MessageResponse(message=result["message"])


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
def reset_password(
    payload: ResetPasswordRequest,
    service: AuthService = Depends(get_auth_service),
):
    result = service.reset_password(
        token=payload.token,
        new_password=payload.new_password,
    )
    return MessageResponse(message=result["message"])