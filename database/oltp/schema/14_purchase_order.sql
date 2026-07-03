/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : purchase_order
Description: Stores purchase orders issued to suppliers.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE purchase_order
(
    purchase_order_id BIGINT GENERATED ALWAYS AS IDENTITY,

    supplier_id BIGINT NOT NULL,

    location_id BIGINT NOT NULL,

    order_date DATE NOT NULL,

    expected_delivery_date DATE,

    purchase_order_status purchase_order_status_type NOT NULL
        DEFAULT 'CREATED',

    total_amount NUMERIC(12,2) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_purchase_order
        PRIMARY KEY (purchase_order_id),

    CONSTRAINT ck_purchase_order_total_amount
        CHECK (total_amount >= 0),

    CONSTRAINT ck_purchase_order_dates
        CHECK (
            expected_delivery_date IS NULL
            OR expected_delivery_date >= order_date
        )
);
