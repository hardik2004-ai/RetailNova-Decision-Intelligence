/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : brand
Description: Stores product brands.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE brand
(
    brand_id BIGINT GENERATED ALWAYS AS IDENTITY,

    brand_name VARCHAR(100) NOT NULL,

    description VARCHAR(500),

    is_active BOOLEAN NOT NULL
        DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_brand
        PRIMARY KEY (brand_id),

    CONSTRAINT uq_brand_name
        UNIQUE (brand_name)
);
