from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.database import get_db
from app.application.schemas.inventory_schemas import UserInventoryAdd, UserInventoryResponse
from app.domain.services.inventory_service import add_card_to_inventory_service, get_user_inventory_service
from app.infrastructure.models.orm_models import UserCardInventoryModel

router = APIRouter()

@router.post("/", response_model=UserInventoryResponse, status_code=status.HTTP_201_CREATED)
def add_card_to_inventory(
    payload: UserInventoryAdd,
    current_user_id: int = 1,
    db: Session = Depends(get_db)
):
    """
    Añade una carta al inventario personal del usuario autenticado.
    """
    return add_card_to_inventory_service(db=db, user_id=current_user_id, data=payload)

@router.get("/{user_id}", response_model=List[UserInventoryResponse])
def get_user_inventory(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_user_inventory_service(db=db, user_id=user_id)