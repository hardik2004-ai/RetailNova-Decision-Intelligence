/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Triggers

File        : update_updated_at_trigger.sql
Description : Creates BEFORE UPDATE triggers to
              automatically maintain updated_at.

Author      : Hardik Narigra
Database    : PostgreSQL 17
==========================================================
*/

-- ======================================================
-- Customer
-- ======================================================

DROP TRIGGER IF EXISTS trg_customer_updated_at ON customer;

CREATE TRIGGER trg_customer_updated_at
BEFORE UPDATE ON customer
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Address
-- ======================================================

DROP TRIGGER IF EXISTS trg_address_updated_at ON address;

CREATE TRIGGER trg_address_updated_at
BEFORE UPDATE ON address
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Membership
-- ======================================================

DROP TRIGGER IF EXISTS trg_membership_updated_at ON membership;

CREATE TRIGGER trg_membership_updated_at
BEFORE UPDATE ON membership
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Category
-- ======================================================

DROP TRIGGER IF EXISTS trg_category_updated_at ON category;

CREATE TRIGGER trg_category_updated_at
BEFORE UPDATE ON category
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Brand
-- ======================================================

DROP TRIGGER IF EXISTS trg_brand_updated_at ON brand;

CREATE TRIGGER trg_brand_updated_at
BEFORE UPDATE ON brand
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Supplier
-- ======================================================

DROP TRIGGER IF EXISTS trg_supplier_updated_at ON supplier;

CREATE TRIGGER trg_supplier_updated_at
BEFORE UPDATE ON supplier
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Product
-- ======================================================

DROP TRIGGER IF EXISTS trg_product_updated_at ON product;

CREATE TRIGGER trg_product_updated_at
BEFORE UPDATE ON product
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Location
-- ======================================================

DROP TRIGGER IF EXISTS trg_location_updated_at ON location;

CREATE TRIGGER trg_location_updated_at
BEFORE UPDATE ON location
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Inventory
-- ======================================================

DROP TRIGGER IF EXISTS trg_inventory_updated_at ON inventory;

CREATE TRIGGER trg_inventory_updated_at
BEFORE UPDATE ON inventory
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Orders
-- ======================================================

DROP TRIGGER IF EXISTS trg_orders_updated_at ON orders;

CREATE TRIGGER trg_orders_updated_at
BEFORE UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Order Item
-- ======================================================

DROP TRIGGER IF EXISTS trg_order_item_updated_at ON order_item;

CREATE TRIGGER trg_order_item_updated_at
BEFORE UPDATE ON order_item
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Payment
-- ======================================================

DROP TRIGGER IF EXISTS trg_payment_updated_at ON payment;

CREATE TRIGGER trg_payment_updated_at
BEFORE UPDATE ON payment
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Return
-- ======================================================

DROP TRIGGER IF EXISTS trg_return_updated_at ON "return";

CREATE TRIGGER trg_return_updated_at
BEFORE UPDATE ON "return"
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Purchase Order
-- ======================================================

DROP TRIGGER IF EXISTS trg_purchase_order_updated_at ON purchase_order;

CREATE TRIGGER trg_purchase_order_updated_at
BEFORE UPDATE ON purchase_order
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();


-- ======================================================
-- Purchase Order Item
-- ======================================================

DROP TRIGGER IF EXISTS trg_purchase_order_item_updated_at ON purchase_order_item;

CREATE TRIGGER trg_purchase_order_item_updated_at
BEFORE UPDATE ON purchase_order_item
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();
