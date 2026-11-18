from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.database import get_db
from app.infrastructure.models.orm_models import CardModel
from app.application.schemas.card_schemas import CardCreate, CardResponse, CardListResponse, CardUpdate
from app.domain.services.card_service import CardService

router = APIRouter(tags=["Cards Catalog"])

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
    """
    Obtiene la lista de cartas con soporte de paginación, filtro por nombre y ordenamiento.
    """
    service = CardService(db)
    cards = service.get_filtered_cards(skip=skip, limit=limit, search=search, order_by=order_by)
    
    # Se ajusta la respuesta al formato de diccionario que espera CardListResponse
    return {
        "total": len(cards),
        "items": cards
    }

@router.get("/{card_id}", response_model=CardResponse)
def get_card_by_id(card_id: int, db: Session = Depends(get_db)):
    """
    Obtiene el detalle de una carta específica según su ID.
    """
    service = CardService(db)
    card = service.get_card_by_id(card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
    return card

@router.put("/{card_id}", response_model=CardResponse)
def update_card(card_id: int, payload: CardUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la información de una carta existente por su ID.
    """
    service = CardService(db)
    updated_card = service.update_card(card_id, payload)
    if not updated_card:
        raise HTTPException(status_code=404, detail="Carta no encontrada para actualizar")
    return updated_card

@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    """
    Elimina una carta del catálogo por su ID.
    """
    service = CardService(db)
    success = service.delete_card(card_id)
    if not success:
        raise HTTPException(status_code=404, detail="Carta no encontrada para eliminar")
    return None
