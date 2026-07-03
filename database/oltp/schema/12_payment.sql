/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : payment
Description: Stores payment details for customer orders.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE payment
(
    payment_id BIGINT GENERATED ALWAYS AS IDENTITY,

    order_id BIGINT NOT NULL,

    payment_method VARCHAR(50) NOT NULL,

    payment_status payment_status_type NOT NULL
        DEFAULT 'PENDING',

    payment_date TIMESTAMPTZ,

    amount NUMERIC(12,2) NOT NULL,

    transaction_reference VARCHAR(100),

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_payment
        PRIMARY KEY (payment_id),

    CONSTRAINT uq_payment_order
        UNIQUE (order_id),

    CONSTRAINT uq_payment_transaction_reference
        UNIQUE (transaction_reference),

    CONSTRAINT ck_payment_amount
        CHECK (amount >= 0)
);
