from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from app.infrastructure.database import Base
import enum


class CardCondition(enum.Enum):
    MINT = "MINT"
    NEAR_MINT = "NEAR_MINT"
    PLAYED = "PLAYED"
    DAMAGED = "DAMAGED"

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False) 
    balance = Column(Float, default=0.0)                           
    role = Column(String, default="collector")           
    
    inventory = relationship("UserCardInventoryModel", back_populates="user", cascade="all, delete-orphan")

class CardModel(Base):
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True) 
    expansion = Column(String, nullable=False) 
    rarity = Column(String, nullable=False) 
    card_number = Column(String, nullable=False)                 
    
    inventories = relationship("UserCardInventoryModel", back_populates="card")

class UserCardInventoryModel(Base):
    __tablename__ = "user_card_inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False) 
    condition = Column(SqlEnum(CardCondition), default=CardCondition.MINT)
    is_for_trade = Column(Boolean, default=True)
    user = relationship("UserModel", back_populates="inventory")
    card = relationship("CardModel", back_populates="inventories")

class TradeOfferModel(Base):
    __tablename__ = "trade_offers"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="PENDING")
    created_at = Column(String, nullable=False)

    items = relationship("TradeOfferItemModel", back_populates="trade_offer")


class TradeOfferItemModel(Base):
    __tablename__ = "trade_offer_items"

    id = Column(Integer, primary_key=True, index=True)
    trade_offer_id = Column(Integer, ForeignKey("trade_offers.id"), nullable=False)
    inventory_item_id = Column(Integer, ForeignKey("user_card_inventory.id"), nullable=False)
    is_offered_by_sender = Column(Boolean, nullable=False) # True si es del sender, False si es del receiver

    trade_offer = relationship("TradeOfferModel", back_populates="items")