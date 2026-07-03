/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : location
Description: Stores retail stores and warehouses.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE location
(
    location_id BIGINT GENERATED ALWAYS AS IDENTITY,

    location_name VARCHAR(150) NOT NULL,

    location_type location_type NOT NULL,

    address VARCHAR(255) NOT NULL,

    city VARCHAR(100) NOT NULL,

    state VARCHAR(100) NOT NULL,

    country VARCHAR(100) NOT NULL,

    postal_code VARCHAR(20) NOT NULL,

    phone_number VARCHAR(20),

    is_active BOOLEAN NOT NULL
        DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_location
        PRIMARY KEY (location_id),

    CONSTRAINT uq_location_name
        UNIQUE (location_name)
);
