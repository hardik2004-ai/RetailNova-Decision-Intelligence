/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : membership
Description: Stores RetailNova Premium membership details
             for customers.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE membership
(
    membership_id BIGINT GENERATED ALWAYS AS IDENTITY,

    customer_id BIGINT NOT NULL,

    membership_number VARCHAR(30) NOT NULL,

    status membership_status_type NOT NULL
        DEFAULT 'ACTIVE',

    start_date DATE NOT NULL,

    end_date DATE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_membership
        PRIMARY KEY (membership_id),

    CONSTRAINT uq_membership_number
        UNIQUE (membership_number),

    CONSTRAINT ck_membership_dates
        CHECK (
            end_date IS NULL
            OR end_date >= start_date
        )
);
