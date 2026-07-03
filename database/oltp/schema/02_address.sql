
/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : address
Description: Stores customer address information.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE address
(
    address_id BIGINT GENERATED ALWAYS AS IDENTITY,

    customer_id BIGINT NOT NULL,

    address_line_1 VARCHAR(150) NOT NULL,
    address_line_2 VARCHAR(150),

    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,

    is_default BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_address
        PRIMARY KEY (address_id)
);
