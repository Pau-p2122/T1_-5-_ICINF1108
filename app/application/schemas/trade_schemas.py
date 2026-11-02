from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TradeOfferCreate(BaseModel):
    receiver_id: int = Field(..., description="ID del usuario que recibe la propuesta")
    offered_inventory_id: int = Field(..., description="ID del ítem del inventario que ofrece el emisor")
    requested_inventory_id: int = Field(..., description="ID del ítem del inventario que solicita al receptor")

class TradeOfferResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    offered_inventory_id: int
    requested_inventory_id: int
    status: str
    created_at: str

    class Config:
        from_attributes = True