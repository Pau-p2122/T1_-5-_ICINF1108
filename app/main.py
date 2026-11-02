from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.routers.auth_router import router as auth_router
from app.presentation.routers.card_router import router as card_router
from app.presentation.routers.inventory_router import router as inventory_router
from app.presentation.routers.trade_router import router as trade_router
from app.domain.exceptions.business_exceptions import BusinessException

def create_app() -> FastAPI:
    app = FastAPI(
        title="TCG Marketplace API",
        description="API REST para la gestión de inventario y mercado de cartas coleccionables",
        version="1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        return JSONResponse(
            status_code=exc.status_code if hasattr(exc, "status_code") else status.HTTP_400_BAD_REQUEST,
            content={
                "error": {
                    "code": getattr(exc, "code", "BUSINESS_RULE_VIOLATION"),
                    "message": exc.message,
                    "details": []
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Los datos enviados no cumplen con el esquema o validaciones requeridas",
                    "details": exc.errors()
                }
            }
        )
    
    app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth & Users"])
    app.include_router(card_router, prefix="/api/v1/cards", tags=["Cards Catalog"])
    app.include_router(inventory_router, prefix="/api/v1/inventory", tags=["User Inventory"])
    app.include_router(trade_router, prefix="/api/v1/trades", tags=["Trades & Market"])

    return app

app = create_app()