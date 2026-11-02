from app.infrastructure.database import SessionLocal
from app.infrastructure.models.orm_models import CardModel

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

if __name__ == "__main__":
    seed_database()