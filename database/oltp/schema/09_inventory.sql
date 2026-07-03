/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : inventory
Description: Stores current inventory levels for products
              at each location.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE inventory
(
    inventory_id BIGINT GENERATED ALWAYS AS IDENTITY,

    product_id BIGINT NOT NULL,

    location_id BIGINT NOT NULL,

    quantity_on_hand INTEGER NOT NULL
        DEFAULT 0,

    reorder_level INTEGER NOT NULL
        DEFAULT 0,

    last_stock_update TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_inventory
        PRIMARY KEY (inventory_id),

    CONSTRAINT uq_inventory_product_location
        UNIQUE (product_id, location_id),

    CONSTRAINT ck_inventory_quantity
        CHECK (quantity_on_hand >= 0),

    CONSTRAINT ck_inventory_reorder_level
        CHECK (reorder_level >= 0)
);
