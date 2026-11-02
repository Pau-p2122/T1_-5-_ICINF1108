from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.infrastructure.models.orm_models import CardModel
from typing import Optional, Dict, Any

def create_card_service(db: Session, data):
    new_card = CardModel(
        name=data.name,
        expansion=data.expansion,
        rarity=data.rarity,
        card_number=data.card_number
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card

def get_cards_service(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    expansion: Optional[str] = None,
    rarity: Optional[str] = None,
    sort_by: str = "id",
    sort_order: str = "asc"
) -> Dict[str, Any]:
    """
    Servicio de negocio para listar cartas con filtros, ordenamiento dinámico y paginación.
    """

    query = db.query(CardModel)

    if expansion:
        query = query.filter(CardModel.expansion.ilike(f"%{expansion}%"))
        
    if rarity:
        query = query.filter(CardModel.rarity.ilike(f"%{rarity}%"))

    allowed_sort_fields = ["id", "name", "expansion", "rarity", "card_number"]
    
    if sort_by in allowed_sort_fields:
        column_attr = getattr(CardModel, sort_by)
        if sort_order.lower() == "desc":
            query = query.order_by(desc(column_attr))
        else:
            query = query.order_by(asc(column_attr))

    total = query.count()
    items = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "limit": limit,
        "offset": skip,
        "items": items
    }