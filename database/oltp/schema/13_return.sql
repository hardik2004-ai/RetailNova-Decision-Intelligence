/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : return
Description: Stores returned order items.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE return
(
    return_id BIGINT GENERATED ALWAYS AS IDENTITY,

    order_item_id BIGINT NOT NULL,

    return_date TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    quantity INTEGER NOT NULL,

    reason VARCHAR(500),

    return_status return_status_type NOT NULL
        DEFAULT 'REQUESTED',

    refund_amount NUMERIC(12,2) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_return
        PRIMARY KEY (return_id),

    CONSTRAINT ck_return_quantity
        CHECK (quantity > 0),

    CONSTRAINT ck_return_refund_amount
        CHECK (refund_amount >= 0)
);
