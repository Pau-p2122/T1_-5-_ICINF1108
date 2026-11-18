# Diagramas del Sistema TCG

## 1. Diagrama de Dominio (Clases y Relaciones)
```mermaid
classDiagram
    class UserModel {
        +int id
        +string email
        +string password_hash
        +float balance
        +string role
    }
    class CardModel {
        +int id
        +string name
        +string expansion
        +string rarity
        +string card_number
    }
    class UserCardInventoryModel {
        +int id
        +int user_id
        +int card_id
        +string condition
        +bool is_for_trade
    }
    class TradeOfferModel {
        +int id
        +int sender_id
        +int receiver_id
        +string status
        +string created_at
    }
    class TradeOfferItemModel {
        +int id
        +int trade_offer_id
        +int inventory_item_id
        +bool is_offered_by_sender
    }
    UserModel "1" --> "*" UserCardInventoryModel : posee
    CardModel "1" --> "*" UserCardInventoryModel : pertenece a
    UserModel "1" --> "*" TradeOfferModel : envía / recibe
    TradeOfferModel "1" --> "*" TradeOfferItemModel : contiene
    UserCardInventoryModel "1" --> "*" TradeOfferItemModel : involucra
    ```
    ## 2. Diagrama de Datos (Modelo Relacional / Entidad-Relación)
    ```mermaid
    erDiagram
    users {
        int id PK
        string email
        string password_hash
        float balance
        string role
    }
    cards {
        int id PK
        string name
        string expansion
        string rarity
        string card_number
    }
    user_card_inventory {
        int id PK
        int user_id FK
        int card_id FK
        string condition
        bool is_for_trade
    }
    trade_offers {
        int id PK
        int sender_id FK
        int receiver_id FK
        string status
        string created_at
    }
    trade_offer_items {
        int id PK
        int trade_offer_id FK
        int inventory_item_id FK
        bool is_offered_by_sender
    }
    users ||--o{ user_card_inventory : "tiene"
    cards ||--o{ user_card_inventory : "cataloga"
    users ||--o{ trade_offers : "envia/recibe"
    trade_offers ||--o{ trade_offer_items : "detalla"
    user_card_inventory ||--o{ trade_offer_items : "participa en"