from app.infrastructure.database import SessionLocal
from app.infrastructure.models.orm_models import CardModel, UserCardInventoryModel, UserModel

def seed_database():
    db = SessionLocal()
    
    existing_cards = db.query(CardModel).count()
    if existing_cards > 0:
        print("El catálogo ya tiene cartas registradas.")
        db.close()
        return

    sample_cards = [
        CardModel(name="Mega Gengar ex", expansion="Ascended Heroes", rarity="Special Illustration Rare", card_number="284"),
        CardModel(name="Pikachu VMAX", expansion="Pitch Black", rarity="Ultra Rare", card_number="050"),
        CardModel(name="Charizard ex", expansion="Ascended Heroes", rarity="Secret Rare", card_number="223"),
        CardModel(name="Mewtwo V", expansion="Base Set", rarity="Holofrare", card_number="075")
    ]

    db.add_all(sample_cards)
    db.commit()
    db.close()
    print("¡Catálogo de cartas sembrado con éxito!")

def seed_user_inventory():
    db = SessionLocal()
    
    user1 = db.query(UserModel).filter(UserModel.id == 1).first()
    if not user1:
        user1 = UserModel(id=1, email="paula@taller.com", password_hash="hash1", balance=100.0, role="collector")
        db.add(user1)

    user2 = db.query(UserModel).filter(UserModel.id == 2).first()
    if not user2:
        user2 = UserModel(id=2, email="alex@taller.com", password_hash="hash2", balance=100.0, role="collector")
        db.add(user2)

    db.commit()


    inv_user2 = db.query(UserCardInventoryModel).filter(UserCardInventoryModel.user_id == 2).first()
    if inv_user2:
        print("El usuario 2 ya tiene inventario registrado.")
        db.close()
        return

    inv_user1_card1 = UserCardInventoryModel(user_id=1, card_id=1, is_for_trade=True)
    inv_user1_card2 = UserCardInventoryModel(user_id=1, card_id=2, is_for_trade=False)
    
    inv_user2_card3 = UserCardInventoryModel(user_id=2, card_id=3, is_for_trade=True)
    inv_user2_card4 = UserCardInventoryModel(user_id=2, card_id=4, is_for_trade=True)

    db.add_all([inv_user1_card1, inv_user1_card2, inv_user2_card3, inv_user2_card4])
    db.commit()
    db.close()
    print("¡Inventarios sembrados correctamente para ambos usuarios!")

if __name__ == "__main__":
    seed_database()
    seed_user_inventory()