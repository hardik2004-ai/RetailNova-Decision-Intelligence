/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Indexes

File        : 01_indexes.sql
Description : Creates performance indexes for OLTP tables.

Author      : Hardik Narigra
Database    : PostgreSQL 17
==========================================================
*/

-- ======================================================
-- Customer
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_customer_email
ON customer (email);

CREATE INDEX IF NOT EXISTS idx_customer_phone
ON customer (phone_number);

CREATE INDEX IF NOT EXISTS idx_customer_created_at
ON customer (created_at);


-- ======================================================
-- Address
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_address_customer
ON address (customer_id);


-- ======================================================
-- Membership
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_membership_customer
ON membership (customer_id);

CREATE INDEX IF NOT EXISTS idx_membership_status
ON membership (status);


-- ======================================================
-- Category
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_category_name
ON category (category_name);


-- ======================================================
-- Brand
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_brand_name
ON brand (brand_name);


-- ======================================================
-- Supplier
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_supplier_name
ON supplier (supplier_name);


-- ======================================================
-- Product
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_product_name
ON product (product_name);

CREATE INDEX IF NOT EXISTS idx_product_category
ON product (category_id);

CREATE INDEX IF NOT EXISTS idx_product_brand
ON product (brand_id);

CREATE INDEX IF NOT EXISTS idx_product_supplier
ON product (supplier_id);


-- ======================================================
-- Location
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_location_type
ON location (location_type);

CREATE INDEX IF NOT EXISTS idx_location_city
ON location (city);

CREATE INDEX IF NOT EXISTS idx_location_state
ON location (state);


-- ======================================================
-- Inventory
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_inventory_product
ON inventory (product_id);

CREATE INDEX IF NOT EXISTS idx_inventory_location
ON inventory (location_id);

CREATE INDEX IF NOT EXISTS idx_inventory_quantity
ON inventory (quantity_on_hand);


-- ======================================================
-- Orders
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_orders_customer
ON orders (customer_id);

CREATE INDEX IF NOT EXISTS idx_orders_location
ON orders (location_id);

CREATE INDEX IF NOT EXISTS idx_orders_order_date
ON orders (order_date);

CREATE INDEX IF NOT EXISTS idx_orders_status
ON orders (order_status);

CREATE INDEX IF NOT EXISTS idx_orders_sales_channel
ON orders (sales_channel);


-- ======================================================
-- Order Item
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_order_item_order
ON order_item (order_id);

CREATE INDEX IF NOT EXISTS idx_order_item_product
ON order_item (product_id);


-- ======================================================
-- Payment
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_payment_order
ON payment (order_id);

CREATE INDEX IF NOT EXISTS idx_payment_status
ON payment (payment_status);

CREATE INDEX IF NOT EXISTS idx_payment_date
ON payment (payment_date);


-- ======================================================
-- Return
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_return_order_item
ON "return" (order_item_id);

CREATE INDEX IF NOT EXISTS idx_return_status
ON "return" (return_status);

CREATE INDEX IF NOT EXISTS idx_return_date
ON "return" (return_date);


-- ======================================================
-- Purchase Order
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_purchase_order_supplier
ON purchase_order (supplier_id);

CREATE INDEX IF NOT EXISTS idx_purchase_order_location
ON purchase_order (location_id);

CREATE INDEX IF NOT EXISTS idx_purchase_order_date
ON purchase_order (order_date);

CREATE INDEX IF NOT EXISTS idx_purchase_order_status
ON purchase_order (purchase_order_status);


-- ======================================================
-- Purchase Order Item
-- ======================================================

CREATE INDEX IF NOT EXISTS idx_purchase_order_item_po
ON purchase_order_item (purchase_order_id);

CREATE INDEX IF NOT EXISTS idx_purchase_order_item_product
ON purchase_order_item (product_id);
