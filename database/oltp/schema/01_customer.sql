/*
===============================================================================
RetailNova Decision Intelligence Platform

Module      : Customer Management
Table       : customer
Description : Stores customer master information.

Author      : Hardik Narigra
Created     : July 2026
===============================================================================
*/

CREATE TABLE customer (

    customer_id         BIGINT GENERATED ALWAYS AS IDENTITY,

    first_name          VARCHAR(50) NOT NULL,

    last_name           VARCHAR(50) NOT NULL,

    email               VARCHAR(255) NOT NULL,

    phone_number        VARCHAR(15),

    date_of_birth       DATE,

    gender              gender_type,

    registration_date   DATE NOT NULL DEFAULT CURRENT_DATE,

    is_active           BOOLEAN NOT NULL DEFAULT TRUE,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT pk_customer
        PRIMARY KEY (customer_id),

    CONSTRAINT uq_customer_email
        UNIQUE (email)

);
