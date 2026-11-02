from sqlalchemy.orm import Session
from app.infrastructure.models.orm_models import TradeOfferModel, UserCardInventoryModel
from app.domain.exceptions.business_exceptions import BusinessException

def create_trade_offer_service(db: Session, sender_id: int, data):
    """
    Servicio para crear una oferta de intercambio validando reglas de negocio.
    """
    if sender_id == data.receiver_id:
        raise BusinessException(
            message="No puedes crear una oferta de intercambio contigo mismo.",
            code="SELF_TRADE_NOT_ALLOWED"
        )

    offered_item = db.query(UserCardInventoryModel).filter(
        UserCardInventoryModel.id == data.offered_inventory_id
    ).first()

    if not offered_item:
        raise BusinessException(message="El ítem ofrecido no existe en el inventario.", code="OFFERED_ITEM_NOT_FOUND")
    
    if offered_item.user_id != sender_id:
        raise BusinessException(message="No puedes ofrecer una carta que no te pertenece.", code="UNAUTHORIZED_CARD_OFFER")
    
    if not offered_item.is_for_trade:
        raise BusinessException(message="La carta ofrecida no está marcada como disponible para intercambio.", code="CARD_NOT_FOR_TRADE")

    requested_item = db.query(UserCardInventoryModel).filter(
        UserCardInventoryModel.id == data.requested_inventory_id
    ).first()

    if not requested_item:
        raise BusinessException(message="El ítem solicitado no existe en el inventario.", code="REQUESTED_ITEM_NOT_FOUND")
    
    if requested_item.user_id != data.receiver_id:
        raise BusinessException(message="El usuario receptor no es dueño de la carta solicitada.", code="INVALID_TARGET_CARD")

    if not requested_item.is_for_trade:
        raise BusinessException(message="La carta solicitada por ti no está disponible para intercambio.", code="TARGET_CARD_NOT_FOR_TRADE")

    new_trade = TradeOfferModel(
        sender_id=sender_id,
        receiver_id=data.receiver_id,
        offered_inventory_id=data.offered_inventory_id,
        requested_inventory_id=data.requested_inventory_id,
        status="PENDING"
    )

    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)

    return new_trade