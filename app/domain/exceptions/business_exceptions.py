class BusinessException(Exception):
    """Excepción base para cualquier regla de negocio infringida."""
    def __init__(self, message: str, status_code: int = 400, error_code: str = "BUSINESS_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)

class InsufficientFundsException(BusinessException):
    def __init__(self, message: str = "El usuario no cuenta con saldo suficiente para esta operación."):
        super().__init__(message=message, status_code=400, error_code="INSUFFICIENT_FUNDS")

class CardNotAvailableException(BusinessException):
    def __init__(self, message: str = "La carta seleccionada no está disponible para intercambio."):
        super().__init__(message=message, status_code=400, error_code="CARD_NOT_AVAILABLE")