from pydantic import BaseModel, Field
from typing import Optional, List

class CardResponse(BaseModel):
    id: int
    name: str
    expansion: str
    rarity: str
    card_number: str

    class Config:
        from_attributes = True

class PaginatedCardsResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[CardResponse]

class CardCreate(BaseModel):
    name: str = Field(..., description="Nombre de la carta")
    expansion: str = Field(..., description="Expansión a la que pertenece la carta")
    rarity: str = Field(..., description="Rareza de la carta")
    card_number: str = Field(..., description="Número de la carta en la expansión")

    class Config:
        from_attributes = True

class CardListResponse(BaseModel):
    total: int
    items: List[CardResponse]

    class Config:
        from_attributes = True