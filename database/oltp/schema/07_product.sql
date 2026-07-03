/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Schema

Table      : product
Description: Stores product information.

Author     : Hardik Narigra
Database   : PostgreSQL 17
==========================================================
*/

CREATE TABLE product
(
    product_id BIGINT GENERATED ALWAYS AS IDENTITY,

    category_id BIGINT NOT NULL,

    brand_id BIGINT NOT NULL,

    supplier_id BIGINT NOT NULL,

    product_name VARCHAR(150) NOT NULL,

    sku VARCHAR(50) NOT NULL,

    barcode VARCHAR(50),

    description VARCHAR(500),

    unit_price NUMERIC(10,2) NOT NULL,

    cost_price NUMERIC(10,2) NOT NULL,

    is_active BOOLEAN NOT NULL
        DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_product
        PRIMARY KEY (product_id),

    CONSTRAINT uq_product_sku
        UNIQUE (sku),

    CONSTRAINT uq_product_barcode
        UNIQUE (barcode),

    CONSTRAINT ck_product_unit_price
        CHECK (unit_price >= 0),

    CONSTRAINT ck_product_cost_price
        CHECK (cost_price >= 0)
);
