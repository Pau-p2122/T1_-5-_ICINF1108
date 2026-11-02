from sqlalchemy.orm import Session
from fastapi import HTTPException, status 
from datetime import datetime
from app.infrastructure.models.orm_models import TradeOfferModel, UserCardInventoryModel
from app.application.schemas.trade_schemas import TradeOfferCreate, TradeOfferItemCreate

def create_trade_offer(db: Session, sender_id: int, offer_data: TradeOfferCreate ):
    if sender_id != sender_id:
        raise HTTPException(
            status_code=status.HTTP_404_FORBIDDEN,
            detail="No tienes permisos para crear una propuesta de intercambio en nombre de otro usuario."
        )
    
    db_trade_offer = TradeOfferModel(
        sender_id=sender_id,
        receiver_id=offer_data.receiver_id,
        status="PENDING",
        created_at=datetime.utcnow().isoformat()
    )
    db.add(db_trade_offer)
    db.commit()
    db.refresh(db_trade_offer)

    for item in offer_data.items:
        inventory_item = db.query(UserCardInventoryModel).filter(
            UserCardInventoryModel.id == item.data.inventory_item_id,
        ).first()
        if not inventory_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El ítem de inventario con ID {item.data.inventory_item_id} no existe."
            )
        expected_owner_id = sender_id if item.data.is_offered_by_sender else offer_data.receiver_id
        if inventory_item.user_id != expected_owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"El ítem de inventario con ID {item.data.inventory_item_id} no pertenece al usuario esperado."
            )
        
        db_trade_offer_item = TradeOfferItemCreate(
            trade_offer_id=db_trade_offer.id,
            inventory_item_id=item.data.inventory_item_id,
            is_offered_by_sender=item.data.is_offered_by_sender  

        )
        db.add(db_trade_offer_item)
    db.commit()
    db.refresh(db_trade_offer)
    return db_trade_offer

def accept_trade_service(db: Session, trade_id: int, current_user_id: int):
    trade = db.query(TradeOfferModel).filter(TradeOfferModel.id == trade_id).first()
    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La oferta de intercambio no existe."
        )

    if trade.receiver_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para aceptar este intercambio."
        )

    if trade.status != "PENDING":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El intercambio ya se encuentra en estado: {trade.status}"
        )

    for item in trade.items:
        inventory_item = db.query(UserCardInventoryModel).filter(
            UserCardInventoryModel.id == item.data.inventory_item_id
        ).first()

        if not inventory_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El ítem de inventario con ID {item.data.inventory_item_id} ya no existe."
            )

        if item.data.is_offered_by_sender:
            inventory_item.user_id = trade.receiver_id
        else:
            inventory_item.user_id = trade.sender_id

    trade.status = "ACCEPTED"
    db.commit()
    db.refresh(trade)
    return {"message": "¡Intercambio aceptado con éxito y cartas transferidas!", "trade_id": trade.id}