from sqlalchemy.orm import Session

from app.domain.exceptions.business_exceptions import BusinessException
from app.infrastructure.repositories.inventory_repository import InventoryRepository


def add_card_to_inventory_service(db: Session, user_id: int, data):
    repo = InventoryRepository(db)
    if not repo.card_exists(data.card_id):
        raise BusinessException(
            message="La carta especificada no existe en el catálogo general.",
            status_code=404,
            error_code="CARD_NOT_FOUND",
        )
    return repo.add(user_id, data.card_id, data.condition, data.is_for_trade)


def get_user_inventory_service(db: Session, user_id: int):
    return InventoryRepository(db).get_by_user(user_id)