from pydantic import BaseModel, EmailStr, Field
from enum import Enum

class ConditionEnum(str, Enum):
    MINT = "MINT"
    NEAR_MINT = "NEAR_MINT"
    PLAYED = "PLAYED"
    DAMAGED = "DAMAGED"

class CardCreateDTO(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    expansion: str = Field(..., min_length=2, max_length=50)
    rarity: str = Field(..., min_length=2, max_length=30)
    card_number: str = Field(..., min_length=1, max_length=10)

class DepositDTO(BaseModel):
    amount: float = Field(..., gt=0.0)

class InventoryAddDTO(BaseModel):
    card_id: int
    condition: ConditionEnum
    is_for_trade: bool = True

class UserRegisterDTO(BaseModel):
 
    email: EmailStr
    password: str = Field(..., min_length=6)