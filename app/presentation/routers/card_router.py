from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.application.schemas.card_schemas import (
    CardCreate,
    CardResponse,
    PaginatedCardsResponse,
)
from app.domain.services.card_service import CardService
from app.infrastructure.database import get_db

router = APIRouter()


@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(payload: CardCreate, db: Session = Depends(get_db)):
    """Crea una nueva carta en el catálogo general."""
    return CardService(db).create_card(payload)


@router.get("/", response_model=PaginatedCardsResponse)
def get_cards(
    skip: int = Query(0, ge=0, description="Registros a omitir"),
    limit: int = Query(10, ge=1, le=100, description="Registros por página"),
    search: str | None = Query(None, description="Filtrar por nombre"),
    expansion: str | None = Query(None, description="Filtrar por expansión"),
    rarity: str | None = Query(None, description="Filtrar por rareza"),
    sort_by: str = Query("id", description="id, name, expansion, rarity o card_number"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
):
    """Lista cartas con filtros, orden y paginación."""
    return CardService(db).get_filtered_cards(
        skip, limit, search, expansion, rarity, sort_by, sort_order
    )
