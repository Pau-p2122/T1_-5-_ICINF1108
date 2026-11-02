from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def auth_status():
    return {"message": "Módulo de autenticación y usuarios activo"}