from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.database import get_db
from app.infrastructure.models.orm_models import CardModel
from app.application.schemas.card_schemas import CardCreate, CardResponse, CardListResponse
from app.domain.services.card_service import create_card_service, get_cards_service

router = APIRouter()

@router.post("/", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
def create_card(payload: CardCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva carta en el catálogo general.
    """
    new_card = create_card_service(db=db, data=payload)
    return new_card

@router.get("/", response_model=CardListResponse)
def get_cards(db: Session = Depends(get_db)):
    """
    Listas de las cartas del catalogo.
    """
    cards = db.query(CardModel).all()
    return { 
       "total": len(cards),
        "items": cards
    } 