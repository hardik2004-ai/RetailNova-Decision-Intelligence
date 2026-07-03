/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Functions

File        : update_updated_at.sql
Description : Reusable trigger function to automatically
              update the updated_at timestamp.

Author      : Hardik Narigra
Database    : PostgreSQL 17
==========================================================
*/

-- ======================================================
-- Function: update_updated_at()
-- ======================================================

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS
$$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;
