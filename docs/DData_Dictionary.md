# RetailNova Enterprise Data Architecture

## Core Business Processes

- Customer Management
- Product Management
- Order Management
- Inventory Management
- Procurement
- Warehouse Operations
- Logistics
- Marketplace Management
- Marketing
- Finance

## Data Sources

| Source | Purpose |
|---------|----------|
| POS | Store Sales |
| Website | Online Orders |
| Mobile App | Customer Activity |
| ERP | Procurement |
| CRM | Customer Profiles |
| WMS | Inventory |
| Finance | Revenue & Expenses |
| Marketing | Campaign Performance |

## Core Business Entities

- Customer
- Product
- Category
- Store
- Warehouse
- Supplier
- Marketplace Seller
- Order
- Order Item
- Payment
- Shipment
- Inventory
- Return
- Promotion

## Dual Architecture

RetailNova follows two logical data models.

### OLTP

Supports operational business processes using normalized tables.

### OLAP

Supports reporting, analytics, machine learning and AI using a dimensional warehouse.

## Data Warehouse Strategy

Methodology:

Kimball Dimensional Modeling

Architecture:

Business Process Bus Architecture

Warehouse Model:

Multiple Star Schemas

Implementation:

Incremental subject-oriented data marts

## Fact Tables

- FactSales
- FactInventory
- FactReturns
- FactMarketing
- FactProcurement

## Dimension Tables

- DimCustomer
- DimProduct
- DimDate
- DimStore
- DimWarehouse
- DimSupplier
- DimSeller
- DimPromotion
- DimRegion

## Conformed Dimensions

Shared dimensions across multiple fact tables.

- Date
- Product
- Customer
- Store
- Warehouse

## Star Schema Decision

RetailNova adopts Kimball Star Schema instead of Snowflake.

Reasons:

- Faster analytical queries
- Simpler SQL
- Better Power BI performance
- Easier business understanding

## Synthetic Data Strategy

RetailNova will generate enterprise data using a hybrid simulation approach.

Components:

- Business Rules
- Probability Models
- Controlled Randomness

The objective is to simulate realistic business behaviour rather than generate random records.

