from pydantic import BaseModel, Field
from typing import Optional

class UserInventoryAdd(BaseModel):
    card_id: int = Field(..., description="ID de la carta del catálogo general")
    condition: str = Field("MINT", description="Condición física de la carta (MINT, NEAR_MINT, PLAYED, etc.)")
    is_for_trade: bool = Field(True, description="Indica si el usuario la puso en el mercado para trueque")

class UserInventoryUpdate(BaseModel):
    is_for_trade: Optional[bool] = None
    condition: Optional[str] = None

class UserInventoryResponse(BaseModel):
    id: int
    user_id: int
    card_id: int
    condition: str
    is_for_trade: bool

    class Config:
        from_attributes = True