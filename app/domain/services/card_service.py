from sqlalchemy.orm import Session

from app.infrastructure.repositories.card_repository import CardRepository


class CardService:
    def __init__(self, db: Session):
        self.repository = CardRepository(db)

    def create_card(self, data):
        return self.repository.create(
            name=data.name,
            expansion=data.expansion,
            rarity=data.rarity,
            card_number=data.card_number,
        )

    def get_filtered_cards(
        self, skip, limit, search, expansion, rarity, sort_by, sort_order
    ):
        total, items = self.repository.get_all(
            skip, limit, search, expansion, rarity, sort_by, sort_order
        )
        return {"total": total, "limit": limit, "offset": skip, "items": items}