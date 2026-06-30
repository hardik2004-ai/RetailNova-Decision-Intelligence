# Database Design

## Document Information

| Field | Value |
|-------|-------|
| Project | RetailNova Decision Intelligence Platform |
| Document | Database Design |
| Database Type | PostgreSQL (OLTP) |
| Design Methodology | Third Normal Form (3NF) |
| Architecture | Enterprise OLTP |
| Version | 1.0 |
| Status | Approved |

---

# Purpose

This document defines the complete operational database (OLTP) design for the RetailNova Decision Intelligence Platform.

The database is designed to:

- Support daily retail business operations
- Maintain data integrity
- Eliminate redundancy through normalization
- Serve as the source system for the analytical data warehouse (OLAP)
- Support business intelligence, machine learning, and AI-driven decision making

---

# Database Design Principles

The RetailNova database follows these principles:

- Business-first design
- Third Normal Form (3NF)
- One source of truth for every entity
- High data integrity
- Minimal redundancy
- Simple and maintainable schema
- Analytics-ready structure
- Enterprise naming standards

---

# Database Architecture

```text
Operational Systems
        │
        ▼
OLTP PostgreSQL Database
        │
        ▼
ETL Pipeline
        │
        ▼
OLAP Data Warehouse
        │
        ▼
SQL Analytics
        │
        ▼
Power BI Dashboards
        │
        ▼
Machine Learning
        │
        ▼
AI Decision Engine
```

---

# Business Modules

| Module | Tables |
|---------|--------|
| Customer Management | Customer, Address, Membership |
| Product Management | Category, Brand, Product |
| Supplier Management | Supplier |
| Location Management | Location |
| Inventory Management | Inventory |
| Sales Management | Order, OrderItem |
| Payment Management | Payment |
| Returns Management | Return |
| Procurement Management | PurchaseOrder, PurchaseOrderItem |

---

# Database Tables

## Customer Management

### Customer

Purpose

Stores customer master information.

Business Value

- Customer analytics
- Customer segmentation
- Revenue analysis
- Customer lifetime value

Primary Key

- customer_id

---

### Address

Purpose

Stores customer addresses.

Business Value

- Shipping
- Geographic analysis
- Regional sales analysis

Primary Key

- address_id

Foreign Key

- customer_id

---

### Membership

Purpose

Stores RetailNova Premium subscriptions.

Business Value

- Membership revenue
- Active members
- Renewal analysis
- Retention analysis

Primary Key

- membership_id

Foreign Key

- customer_id

---

# Product Management

### Category

Purpose

Groups products into categories.

Business Value

- Category performance
- Category profitability
- Category inventory

Primary Key

- category_id

---

### Brand

Purpose

Stores product brands.

Business Value

- Brand performance
- Brand sales analysis

Primary Key

- brand_id

---

### Product

Purpose

Stores product master information.

Business Value

- Product analytics
- Inventory
- Sales
- Procurement

Primary Key

- product_id

Foreign Keys

- category_id
- brand_id
- supplier_id

---

# Supplier Management

### Supplier

Purpose

Stores supplier information.

Business Value

- Procurement analysis
- Supplier performance
- Cost analysis

Primary Key

- supplier_id

---

# Location Management

### Location

Purpose

Stores all physical locations.

Location Types

- STORE
- WAREHOUSE

Business Value

- Store analytics
- Warehouse analytics
- Regional analytics

Primary Key

- location_id

---

# Inventory Management

### Inventory

Purpose

Stores current inventory for every product at every location.

Business Value

- Inventory value
- Low stock analysis
- Stock availability
- Reorder recommendations

Primary Key

- inventory_id

Foreign Keys

- product_id
- location_id

---

# Sales Management

### Order

Purpose

Stores customer orders.

Business Value

- Revenue
- Sales
- Order trends
- Customer purchases

Primary Key

- order_id

Foreign Keys

- customer_id
- location_id

---

### OrderItem

Purpose

Stores products inside each order.

Business Value

- Product sales
- Quantity sold
- Product profitability

Primary Key

- order_item_id

Foreign Keys

- order_id
- product_id

---

# Payment Management

### Payment

Purpose

Stores payment information.

Business Value

- Revenue
- Payment analysis
- Payment success rate

Primary Key

- payment_id

Foreign Key

- order_id

---

# Returns Management

### Return

Purpose

Stores returned products.

Business Value

- Return rate
- Product quality
- Supplier quality
- Refund analysis

Primary Key

- return_id

Foreign Key

- order_item_id

---

# Procurement Management

### PurchaseOrder

Purpose

Stores supplier purchase orders.

Business Value

- Procurement spending
- Supplier analysis

Primary Key

- purchase_order_id

Foreign Key

- supplier_id

---

### PurchaseOrderItem

Purpose

Stores products purchased from suppliers.

Business Value

- Purchase history
- Cost analysis

Primary Key

- purchase_order_item_id

Foreign Keys

- purchase_order_id
- product_id

---

# Relationship Summary

| Parent | Child | Relationship |
|---------|-------|-------------|
| Customer | Address | One to Many |
| Customer | Membership | One to Many |
| Customer | Order | One to Many |
| Category | Product | One to Many |
| Brand | Product | One to Many |
| Supplier | Product | One to Many |
| Supplier | PurchaseOrder | One to Many |
| PurchaseOrder | PurchaseOrderItem | One to Many |
| Product | PurchaseOrderItem | One to Many |
| Product | Inventory | One to Many |
| Location | Inventory | One to Many |
| Location | Order | One to Many |
| Order | OrderItem | One to Many |
| Product | OrderItem | One to Many |
| Order | Payment | One to One |
| OrderItem | Return | Zero or One |

---

# Normalization

The RetailNova OLTP database is fully normalized to Third Normal Form (3NF).

## First Normal Form (1NF)

- Atomic values
- No repeating groups
- Unique primary keys

## Second Normal Form (2NF)

- Every non-key attribute depends on the whole primary key

## Third Normal Form (3NF)

- No transitive dependencies
- No redundant attributes
- Every attribute depends only on its primary key

---

# Naming Conventions

## Tables

- Singular names
- PascalCase

Examples

- Customer
- Product
- Order
- Payment

---

## Columns

snake_case

Examples

- customer_id
- order_date
- created_at
- updated_at

---

## Primary Keys

Format

```
table_name_id
```

Examples

- customer_id
- product_id
- order_id

---

## Foreign Keys

Use the referenced primary key name.

Examples

- customer_id
- supplier_id
- category_id
- location_id

---

# Audit Columns

Every transactional and master table includes:

- created_at
- updated_at

Purpose

- Record creation timestamp
- Record modification timestamp
- Support auditing
- Support ETL

---

# Business Rules

## Customer

- One customer can have multiple addresses.
- One customer can have one active membership at a time.
- One customer can place many orders.

---

## Product

- One product belongs to one category.
- One product belongs to one brand.
- One product has one primary supplier.

---

## Location

- Location type is STORE or WAREHOUSE.
- Inventory belongs to one location.

---

## Inventory

- Quantity cannot be negative.
- Every inventory record belongs to one product and one location.

---

## Orders

- One order belongs to one customer.
- One order belongs to one location.
- One order contains one or more products.
- Every order has exactly one payment.
- Every order has one sales channel.

Sales Channels

- STORE
- WEBSITE
- MOBILE_APP
- MARKETPLACE

---

## Payment

- One payment belongs to one order.
- No partial payments.
- One payment per order.

Payment Methods

- UPI
- Credit Card
- Debit Card
- Net Banking
- Wallet
- Cash

---

## Returns

- Returns reference an OrderItem.
- One OrderItem can be returned only once.

---

## Procurement

- One supplier can receive many purchase orders.
- One purchase order contains one or more products.

---

# Major Design Decisions

| Decision | Reason |
|-----------|--------|
| Unified Location table | Simplified Store and Warehouse management |
| Removed MembershipPlan | Only one RetailNova Premium subscription with monthly/yearly billing |
| Removed InventoryMovement | Current inventory is sufficient for analytics |
| Removed ReturnItem | Return references OrderItem directly |
| One Payment per Order | Simpler payment model |
| One Supplier per Product | Avoid unnecessary many-to-many relationships |
| No Country column | Version 1 operates only in India |
| No Manager field in Location | Not required for business analytics |
| No lookup tables for status values | Simple CHECK constraints are sufficient |

---

# Final Database Statistics

| Metric | Value |
|---------|------:|
| Business Modules | 9 |
| Tables | 15 |
| Primary Keys | 15 |
| Foreign Key Relationships | 16 |
| Database Type | OLTP |
| Normalization | Third Normal Form (3NF) |

---

# Future Enhancements

The following features are intentionally excluded from Version 1 to keep the database focused and maintainable:

- Employee Management
- Product Reviews
- Shopping Cart
- Coupons
- Wishlists
- Multi-supplier products
- Inventory movement history
- Stock transfers
- Supplier invoices
- Multiple payment attempts
- Partial payments
- Loyalty points
- Multi-country support

These can be added in future versions without requiring major changes to the existing database design.

---

# Conclusion

The RetailNova OLTP database is designed as a clean, normalized, enterprise-ready operational database that supports core retail business processes while providing a robust foundation for downstream analytics, reporting, machine learning, and AI-driven decision support. Every table has a clear business purpose, every relationship supports operational workflows, and the overall schema balances simplicity with enterprise-grade design principles.
