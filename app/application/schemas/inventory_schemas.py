from pydantic import BaseModel, Field
from typing import Optional, List
from app.application.schemas.card_schemas import CardResponse

class UserInventoryAdd(BaseModel):
    card_id: int = Field(..., description="ID de la carta del catálogo general")
    condition: str = Field("MINT", description="Condición física de la carta (MINT, NEAR_MINT, PLAYED, etc.)")
    is_for_trade: bool = Field(True, description="Indica si el usuario la puso en el mercado para trueque")

class UserInventoryUpdate(BaseModel):
    is_for_trade: Optional[bool] = None
    condition: Optional[str] = None

class UserInventoryItemResponse(BaseModel):
    id: int
    user_id: int
    card_id: int
    condition: str
    is_for_trade: bool
    card: CardResponse # Incluye los detalles de la carta gracias a la relación ORM

    class Config:
        from_attributes = True

class UserInventoryResponse(BaseModel):
    user_id: int
    total_items: int
    items: List[UserInventoryItemResponse]

    class Config:
        from_attributes = True