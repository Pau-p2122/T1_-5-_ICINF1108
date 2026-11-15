from sqlalchemy.orm import Session
from app.infrastructure.models.orm_models import CardModel

class CardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 10, search: str | None = None, order_by: str = "id"):
        query = self.db.query(CardModel)

        # Aplicar filtro de búsqueda por nombre si existe
        if search:
            query = query.filter(CardModel.name.ilike(f"%{search}%"))

        # Aplicar ordenamiento dinámico
        if hasattr(CardModel, order_by):
            query = query.order_by(getattr(CardModel, order_by))

        return query.offset(skip).limit(limit).all()
