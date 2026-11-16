from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.infrastructure.models.orm_models import CardModel

SORT_FIELDS = ["id", "name", "expansion", "rarity", "card_number"]


class CardRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, expansion: str, rarity: str, card_number: str):
        card = CardModel(
            name=name, expansion=expansion, rarity=rarity, card_number=card_number
        )
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def get_all(self, skip, limit, search, expansion, rarity, sort_by, sort_order):
        query = self.db.query(CardModel)

        if search:
            query = query.filter(CardModel.name.ilike(f"%{search}%"))
        if expansion:
            query = query.filter(CardModel.expansion.ilike(f"%{expansion}%"))
        if rarity:
            query = query.filter(CardModel.rarity.ilike(f"%{rarity}%"))

        if sort_by in SORT_FIELDS:
            column = getattr(CardModel, sort_by)
            query = query.order_by(desc(column) if sort_order == "desc" else asc(column))

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return total, items