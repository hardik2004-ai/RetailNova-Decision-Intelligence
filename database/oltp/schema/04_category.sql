/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : category
Description: Stores product categories.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE category
(
    category_id BIGINT GENERATED ALWAYS AS IDENTITY,

    category_name VARCHAR(100) NOT NULL,

    description VARCHAR(500),

    is_active BOOLEAN NOT NULL
        DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_category
        PRIMARY KEY (category_id),

    CONSTRAINT uq_category_name
        UNIQUE (category_name)
);
