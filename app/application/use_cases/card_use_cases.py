from app.infrastructure.repositories.card_repository import CardRepository

class GetCardsUseCase:
    def __init__(self, card_repository: CardRepository):
        self.card_repository = card_repository

    def execute(self, skip: int = 0, limit: int = 10, search: str | None = None, order_by: str | None = None):
        """
        Ejecuta la lógica de negocio para obtener las cartas del catálogo aplicando filtros y paginación.
        """
        return self.card_repository.get_all(skip=skip, limit=limit, search=search, order_by=order_by)