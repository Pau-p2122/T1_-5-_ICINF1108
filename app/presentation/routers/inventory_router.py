from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.schemas.inventory_schemas import UserInventoryAdd, UserInventoryItemResponse, UserInventoryResponse
from app.domain.services.inventory_service import add_card_to_inventory_service, get_user_inventory_service

router = APIRouter(tags=["User Inventory"])

@router.post("/", response_model=UserInventoryItemResponse, status_code=status.HTTP_201_CREATED)
def add_card_to_inventory(
    payload: UserInventoryAdd,
    current_user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Añade una carta al inventario personal del usuario autenticado.
    """
    return add_card_to_inventory_service(db=db, user_id=current_user_id, data=payload)

@router.get("/{user_id}", response_model=UserInventoryResponse)
def get_user_inventory(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene el inventario completo de cartas de un usuario con su conteo total.
    """
    return get_user_inventory_service(db=db, user_id=user_id)