from sqlalchemy.orm import Session
from app.infrastructure.models.orm_models import UserCardInventoryModel, CardModel
from app.application.schemas.inventory_schemas import UserInventoryAdd

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def check_card_exists(self, card_id: int):
        return self.db.query(CardModel).filter(CardModel.id == card_id).first()

    def add_to_inventory(self, user_id: int, data: UserInventoryAdd):
        inventory_item = UserCardInventoryModel(
            user_id=user_id,
            card_id=data.card_id,
            condition=data.condition,
            is_for_trade=data.is_for_trade
        )
        self.db.add(inventory_item)
        self.db.commit()
        self.db.refresh(inventory_item)
        return inventory_item

    def get_by_user_id(self, user_id: int):
        return self.db.query(UserCardInventoryModel).filter(UserCardInventoryModel.user_id == user_id).all()
