from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.database import get_db
from app.infrastructure.models.orm_models import CardModel
from app.application.schemas.card_schemas import CardCreate, CardResponse, CardListResponse
from app.domain.services.card_service import CardService # Asegúrate de importar tu clase o función de servicio correctamente

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(payload: CardCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva carta en el catálogo general.
    """
    service = CardService(db)
    return service.create_card(payload)

@router.get("/", response_model=CardListResponse)
def get_cards(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Límite por página"),
    search: str | None = Query(None, description="Filtrar por nombre de carta"),
    order_by: str | None = Query("id", description="Campo para ordenar"),
    db: Session = Depends(get_db)
):
    """
    Obtiene la lista de cartas con soporte de paginación, filtro por nombre y ordenamiento.
    """
    service = CardService(db)
    return service.get_filtered_cards(skip=skip, limit=limit, search=search, order_by=order_by)
