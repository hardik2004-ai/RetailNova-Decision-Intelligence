/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : supplier
Description: Stores supplier information.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE supplier
(
    supplier_id BIGINT GENERATED ALWAYS AS IDENTITY,

    supplier_name VARCHAR(150) NOT NULL,

    contact_person VARCHAR(150),

    email VARCHAR(255),

    phone_number VARCHAR(20),

    address VARCHAR(255),

    city VARCHAR(100),

    state VARCHAR(100),

    country VARCHAR(100),

    postal_code VARCHAR(20),

    is_active BOOLEAN NOT NULL
        DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_supplier
        PRIMARY KEY (supplier_id),

    CONSTRAINT uq_supplier_name
        UNIQUE (supplier_name),

    CONSTRAINT uq_supplier_email
        UNIQUE (email)
);
