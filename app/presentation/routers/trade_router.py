from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.application.schemas.trade_schemas import TradeOfferCreate, TradeOfferResponse
from app.domain.services.trade_service import create_trade_offer_service

router = APIRouter()

@router.post("/", response_model=TradeOfferResponse, status_code=status.HTTP_201_CREATED)
def create_trade(
    payload: TradeOfferCreate,
    current_user_id: int = 1, 
    db: Session = Depends(get_db)
):
    """
    Crea una nueva propuesta de intercambio de cartas entre usuarios.
    """
    trade = create_trade_offer_service(db=db, sender_id=current_user_id, data=payload)
    return trade