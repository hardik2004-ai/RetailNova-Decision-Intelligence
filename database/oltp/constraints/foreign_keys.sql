/*
==========================================================
RetailNova Decision Intelligence Platform
OLTP Database Constraints

File        : foreign_keys.sql
Description : Creates all foreign key constraints.

Author      : Hardik Narigra
Database    : PostgreSQL 17
==========================================================
*/

-- ======================================================
-- Address
-- ======================================================

ALTER TABLE address
ADD CONSTRAINT fk_address_customer
FOREIGN KEY (customer_id)
REFERENCES customer(customer_id);

-- ======================================================
-- Membership
-- ======================================================

ALTER TABLE membership
ADD CONSTRAINT fk_membership_customer
FOREIGN KEY (customer_id)
REFERENCES customer(customer_id);

-- ======================================================
-- Product
-- ======================================================

ALTER TABLE product
ADD CONSTRAINT fk_product_category
FOREIGN KEY (category_id)
REFERENCES category(category_id);

ALTER TABLE product
ADD CONSTRAINT fk_product_brand
FOREIGN KEY (brand_id)
REFERENCES brand(brand_id);

ALTER TABLE product
ADD CONSTRAINT fk_product_supplier
FOREIGN KEY (supplier_id)
REFERENCES supplier(supplier_id);

-- ======================================================
-- Inventory
-- ======================================================

ALTER TABLE inventory
ADD CONSTRAINT fk_inventory_product
FOREIGN KEY (product_id)
REFERENCES product(product_id);

ALTER TABLE inventory
ADD CONSTRAINT fk_inventory_location
FOREIGN KEY (location_id)
REFERENCES location(location_id);

-- ======================================================
-- Orders
-- ======================================================

ALTER TABLE orders
ADD CONSTRAINT fk_orders_customer
FOREIGN KEY (customer_id)
REFERENCES customer(customer_id);

ALTER TABLE orders
ADD CONSTRAINT fk_orders_location
FOREIGN KEY (location_id)
REFERENCES location(location_id);

-- ======================================================
-- Order Item
-- ======================================================

ALTER TABLE order_item
ADD CONSTRAINT fk_order_item_order
FOREIGN KEY (order_id)
REFERENCES orders(order_id);

ALTER TABLE order_item
ADD CONSTRAINT fk_order_item_product
FOREIGN KEY (product_id)
REFERENCES product(product_id);

-- ======================================================
-- Payment
-- ======================================================

ALTER TABLE payment
ADD CONSTRAINT fk_payment_order
FOREIGN KEY (order_id)
REFERENCES orders(order_id);

-- ======================================================
-- Return
-- ======================================================

ALTER TABLE return
ADD CONSTRAINT fk_return_order_item
FOREIGN KEY (order_item_id)
REFERENCES order_item(order_item_id);

-- ======================================================
-- Purchase Order
-- ======================================================

ALTER TABLE purchase_order
ADD CONSTRAINT fk_purchase_order_supplier
FOREIGN KEY (supplier_id)
REFERENCES supplier(supplier_id);

ALTER TABLE purchase_order
ADD CONSTRAINT fk_purchase_order_location
FOREIGN KEY (location_id)
REFERENCES location(location_id);

-- ======================================================
-- Purchase Order Item
-- ======================================================

ALTER TABLE purchase_order_item
ADD CONSTRAINT fk_purchase_order_item_purchase_order
FOREIGN KEY (purchase_order_id)
REFERENCES purchase_order(purchase_order_id);

ALTER TABLE purchase_order_item
ADD CONSTRAINT fk_purchase_order_item_product
FOREIGN KEY (product_id)
REFERENCES product(product_id);
