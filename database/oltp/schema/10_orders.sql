/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : orders
Description: Stores customer orders.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE orders
(
    order_id BIGINT GENERATED ALWAYS AS IDENTITY,

    customer_id BIGINT NOT NULL,

    location_id BIGINT NOT NULL,

    order_date TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    sales_channel sales_channel_type NOT NULL,

    order_status order_status_type NOT NULL
        DEFAULT 'PENDING',

    total_amount NUMERIC(12,2) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_orders
        PRIMARY KEY (order_id),

    CONSTRAINT ck_orders_total_amount
        CHECK (total_amount >= 0)
);
