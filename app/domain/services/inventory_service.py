from sqlalchemy.orm import Session
from app.domain.exceptions.business_exceptions import BusinessException
from app.infrastructure.repositories.inventory_repository import InventoryRepository


def add_card_to_inventory_service(db: Session, user_id: int, data):
    """
    Agrega una carta del catálogo al inventario personal de un usuario usando el repositorio.
    """
    repo = InventoryRepository(db)
    
    # Validar regla de negocio a través del repositorio
    card = repo.check_card_exists(data.card_id)
    if not card:
        raise BusinessException(message="La carta especificada no existe en el catálogo general.", code="CARD_NOT_FOUND")
    
    # Delegar la persistencia al repositorio
    return repo.add_to_inventory(user_id, data)

def get_user_inventory_service(db: Session, user_id: int):
    """
    Obtiene el inventario completo de cartas de un usuario con su conteo total usando el repositorio.
    """
    repo = InventoryRepository(db)
    items = repo.get_by_user_id(user_id)
    
    return {
        "user_id": user_id,
        "total_items": len(items),
        "items": items
    }
