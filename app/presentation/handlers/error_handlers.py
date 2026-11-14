from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.exceptions.business_exceptions import BusinessException

async def business_exception_handler(request: Request, exc: BusinessException):
    """
    Intercepta cualquier BusinessException lanzada en los servicios
    y devuelve una respuesta HTTP estructurada y unificada.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message
            }
        }
    )