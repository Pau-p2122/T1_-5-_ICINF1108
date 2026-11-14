from sqlalchemy.orm import Session
from app.infrastructure.models.orm_models import UserCardInventoryModel, CardModel
from app.domain.exceptions.business_exceptions import BusinessException

def add_card_to_inventory_service(db: Session, user_id: int, data):
    """
    Agrega una carta del catálogo al inventario personal de un usuario.
    """
    card = db.query(CardModel).filter(CardModel.id == data.card_id).first()
    if not card:
        raise BusinessException(message="La carta especificada no existe en el catálogo general.", code="CARD_NOT_FOUND")
    inventory_item = UserCardInventoryModel(
        user_id=user_id,
        card_id=data.card_id,
        condition=data.condition,
        is_for_trade=data.is_for_trade
    )

    db.add(inventory_item)
    db.commit()
    db.refresh(inventory_item)

    return inventory_item

def get_user_inventory_service(db: Session, user_id: int):
    return db.query(UserCardInventoryModel).filter(UserCardInventoryModel.user_id == user_id).all()