from sqlalchemy.orm import Session

from app.infrastructure.models.orm_models import CardModel, UserCardInventoryModel


class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def card_exists(self, card_id: int) -> bool:
        return (
            self.db.query(CardModel).filter(CardModel.id == card_id).first()
            is not None
        )

    def add(self, user_id: int, card_id: int, condition: str, is_for_trade: bool):
        item = UserCardInventoryModel(
            user_id=user_id,
            card_id=card_id,
            condition=condition,
            is_for_trade=is_for_trade,
        )
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_by_user(self, user_id: int):
        return (
            self.db.query(UserCardInventoryModel)
            .filter(UserCardInventoryModel.user_id == user_id)
            .all()
        )