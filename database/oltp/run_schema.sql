/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Master Script

File        : run_schema.sql
Description : Executes all OLTP schema components in
              correct dependency order.

Author      : Hardik Narigra
Database    : PostgreSQL 17
==========================================================
*/

-- ======================================================
-- STEP 1: ENUM TYPES
-- ======================================================
\i schema/00_types.sql


-- ======================================================
-- STEP 2: CORE TABLES
-- ======================================================
\i schema/01_customer.sql
\i schema/02_address.sql
\i schema/03_membership.sql
\i schema/04_category.sql
\i schema/05_brand.sql
\i schema/06_supplier.sql
\i schema/07_product.sql
\i schema/08_location.sql
\i schema/09_inventory.sql
\i schema/10_orders.sql
\i schema/11_order_item.sql
\i schema/12_payment.sql
\i schema/13_return.sql
\i schema/14_purchase_order.sql
\i schema/15_purchase_order_item.sql


-- ======================================================
-- STEP 3: CONSTRAINTS (FOREIGN KEYS)
-- ======================================================
\i constraints/foreign_keys.sql


-- ======================================================
-- STEP 4: INDEXES
-- ======================================================
\i indexes/01_indexes.sql


-- ======================================================
-- STEP 5: FUNCTIONS
-- ======================================================
\i functions/update_updated_at.sql


-- ======================================================
-- STEP 6: TRIGGERS
-- ======================================================
\i triggers/update_updated_at_trigger.sql


-- ======================================================
-- FINAL MESSAGE
-- ======================================================
SELECT 'RetailNova OLTP Schema Deployment Completed Successfully' AS status;
