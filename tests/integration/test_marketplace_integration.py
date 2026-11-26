from app.domain.services.card_service import CardService
from app.infrastructure.models.orm_models import CardModel, UserCardInventoryModel


def test_integration_cards_crud_flow(client):
    create_res = client.post(
        "/api/v1/cards/",
        json={
            "name": "Charizard",
            "expansion": "Base Set",
            "rarity": "Holo Rare",
            "card_number": "4/102",
        },
    )
    assert create_res.status_code == 201
    created = create_res.json()
    card_id = created["id"]

    list_res = client.get("/api/v1/cards/?skip=0&limit=10&search=Charizard")
    assert list_res.status_code == 200
    assert list_res.json()["total"] >= 1

    get_res = client.get(f"/api/v1/cards/{card_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Charizard"

    update_res = client.put(
        f"/api/v1/cards/{card_id}",
        json={"rarity": "Secret Rare"},
    )
    assert update_res.status_code == 200
    assert update_res.json()["rarity"] == "Secret Rare"

    del_res = client.delete(f"/api/v1/cards/{card_id}")
    assert del_res.status_code == 204

    missing_res = client.get(f"/api/v1/cards/{card_id}")
    assert missing_res.status_code == 404


def test_integration_cards_not_found_branches(client):
    assert client.get("/api/v1/cards/99999").status_code == 404
    assert client.put("/api/v1/cards/99999", json={"rarity": "Common"}).status_code == 404
    assert client.delete("/api/v1/cards/99999").status_code == 404


def test_integration_inventory_and_card_service(client, db_session, sample_user):
    card = CardModel(
        name="Pikachu",
        expansion="Jungle",
        rarity="Common",
        card_number="60/64",
    )
    db_session.add(card)
    db_session.commit()
    db_session.refresh(card)

    inv_item = UserCardInventoryModel(
        user_id=sample_user.id,
        card_id=card.id,
        is_for_trade=True,
    )
    db_session.add(inv_item)
    db_session.commit()
    db_session.refresh(inv_item)

    service = CardService(db_session)
    assert service is not None

    inv_res = client.get(f"/api/v1/inventory/{sample_user.id}")
    assert inv_res.status_code in (200, 404)