from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.schemas.trade_schemas import TradeOfferCreate, TradeOfferResponse, TradeOfferItemResponse, TradeOfferItemCreate
from app.domain.services.trade_service import create_trade_offer, accept_trade_service

router = APIRouter()

@router.post("/", response_model=TradeOfferResponse, status_code=status.HTTP_201_CREATED)
def create_trade(
    current_user_id: int,
    offer_data: TradeOfferCreate,
    db: Session = Depends(get_db)
):
    """
    Crea una nueva propuesta de intercambio de cartas entre usuarios.
    """
    return create_trade_offer(db=db, sender_id=current_user_id, offer_data=offer_data)

@router.post("/{trade_id}/accept")
def accept_trade(
    trade_id: int,
    current_user_id: int = Query(..., description="ID del usuario autenticado que acepta la propuesta de intercambio"),
    db: Session = Depends(get_db)
):
    """
    Permite al usuario receptor aceptar una propuesta de intercambio pendiente.
    """
    return accept_trade_service(db=db, trade_id=trade_id, current_user_id=current_user_id)
             