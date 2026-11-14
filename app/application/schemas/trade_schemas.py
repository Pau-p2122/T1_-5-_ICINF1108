from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class TradeOfferItemCreate(BaseModel):
    inventory_item_id: int = Field(..., description="ID del ítem en el inventario")
    is_offered_by_sender: bool = Field(..., description="True si la carta es del emisor, False si es del receptor")

class TradeOfferCreate(BaseModel):
    receiver_id: int = Field(..., description="ID del usuario que recibe la propuesta de intercambio")
    items: List[TradeOfferItemCreate] = Field(..., description="Lista de cartas involucradas en el trueque (ofrecidas y solicitadas)")

class TradeOfferItemResponse(BaseModel):
    id: int
    trade_offer_id: int
    inventory_item_id: int
    is_offered_by_sender: bool

    class Config:
        from_attributes = True

class TradeOfferResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    status: str
    created_at: str
    items: List[TradeOfferItemResponse] = []

    class Config:
        from_attributes = True