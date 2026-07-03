/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : purchase_order_item
Description: Stores items included in purchase orders.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE purchase_order_item
(
    purchase_order_item_id BIGINT GENERATED ALWAYS AS IDENTITY,

    purchase_order_id BIGINT NOT NULL,

    product_id BIGINT NOT NULL,

    quantity INTEGER NOT NULL,

    unit_cost NUMERIC(10,2) NOT NULL,

    line_total NUMERIC(12,2) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_purchase_order_item
        PRIMARY KEY (purchase_order_item_id),

    CONSTRAINT ck_purchase_order_item_quantity
        CHECK (quantity > 0),

    CONSTRAINT ck_purchase_order_item_unit_cost
        CHECK (unit_cost >= 0),

    CONSTRAINT ck_purchase_order_item_line_total
        CHECK (line_total >= 0)
);
