/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : order_item
Description: Stores individual items within an order.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE order_item
(
    order_item_id BIGINT GENERATED ALWAYS AS IDENTITY,

    order_id BIGINT NOT NULL,

    product_id BIGINT NOT NULL,

    quantity INTEGER NOT NULL,

    unit_price NUMERIC(10,2) NOT NULL,

    discount_amount NUMERIC(10,2) NOT NULL
        DEFAULT 0,

    line_total NUMERIC(12,2) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_order_item
        PRIMARY KEY (order_item_id),

    CONSTRAINT ck_order_item_quantity
        CHECK (quantity > 0),

    CONSTRAINT ck_order_item_unit_price
        CHECK (unit_price >= 0),

    CONSTRAINT ck_order_item_discount
        CHECK (discount_amount >= 0),

    CONSTRAINT ck_order_item_line_total
        CHECK (line_total >= 0)
);
