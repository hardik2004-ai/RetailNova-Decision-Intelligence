# RetailNova Meeting Notes

## Purpose

This document captures the key discussions, architectural reviews, decisions, and outcomes from each project session.

---

# Day 1 — Project Foundation

**Date:** Day 1

## Agenda

* Project selection
* Business domain selection
* Repository planning
* Project vision
* Technology stack
* Development philosophy

---

## Discussion

* Evaluated multiple project ideas.
* Selected an enterprise retail domain due to its rich business processes.
* Decided to build a Decision Intelligence Platform instead of a traditional dashboard project.
* Discussed long-term roadmap and portfolio goals.

---

## Key Decisions

* Retail Industry selected.
* Enterprise Decision Intelligence Platform approved.
* PostgreSQL selected.
* Python selected.
* Power BI selected.
* Streamlit selected.
* Synthetic enterprise dataset approved.
* Business-first development methodology adopted.

---

## Outcome

Business foundation established.

---

# Day 2 — Business Architecture

**Date:** Day 2

## Agenda

* Business Requirements Document
* Company profile
* Business objectives
* KPIs
* Business questions
* Stakeholders
* Repository documentation

---

## Discussion

* Defined RetailNova as a fictional omnichannel retail company.
* Identified strategic and operational business problems.
* Defined measurable objectives.
* Identified business stakeholders.
* Created repository documentation structure.

---

## Key Decisions

* Single BRD document.
* Separate architecture documentation.
* Separate decision log.
* GitHub-first documentation approach.

---

## Outcome

Business Requirements Document Version 1 completed.

---

# Day 3 — Enterprise Data Architecture

**Date:** Day 3

## Agenda

* Business process mapping
* Enterprise systems
* Data source inventory
* Business entities
* Relationships
* OLTP vs OLAP
* Warehouse strategy
* Fact & Dimension modeling
* Star schema
* Data dictionary
* Synthetic data strategy

---

## Discussion

### Business Processes

Identified all major enterprise business processes including:

* Customer Management
* Product Management
* Order Management
* Inventory Management
* Procurement
* Warehouse Operations
* Logistics
* Marketing
* Finance
* Marketplace Management

---

### Enterprise Systems

Discussed internal operational systems.

* ERP
* CRM
* POS
* OMS
* WMS
* Finance System
* Marketing Automation

---

### Logical Architecture

Reviewed the separation between operational processing and analytical processing.

Discussed:

* OLTP
* OLAP
* ETL
* Enterprise Data Warehouse

---

### Warehouse Strategy

Compared:

* Inmon
* Kimball
* Data Vault

Approved Kimball Dimensional Modeling.

---

### Fact & Dimension Modeling

Identified candidate fact tables.

* FactSales
* FactInventory
* FactReturns
* FactMarketing
* FactProcurement

Identified core dimensions.

* Customer
* Product
* Store
* Warehouse
* Date
* Supplier
* Promotion
* Seller

---

### Star Schema

Compared:

* Star Schema
* Snowflake Schema

Approved Star Schema using Kimball Bus Architecture.

---

### Data Dictionary

Defined:

* Business Glossary
* KPI Dictionary
* Naming Standards
* Data Standards
* Data Lineage

---

### Synthetic Dataset Strategy

Discussed multiple approaches.

Compared:

* Random generation
* Rule-based generation
* Probability-based generation

Approved hybrid simulation using business rules, probability models, and controlled randomness.

---

## Key Decisions

* Dual Logical Architecture
* Kimball Warehouse
* Multiple Star Schemas
* Subject-oriented warehouse
* Hybrid enterprise data generation
* Incremental development sprints

---

## Outcome

Enterprise Data Architecture completed.

RetailNova is now ready for database engineering.

---

# Day 5 — OLTP Database Engineering

**Date:** Day 5

## Agenda

* PostgreSQL OLTP schema implementation
* Foreign key implementation
* Performance indexing
* Audit automation
* Deployment preparation

---

## Discussion

### OLTP Schema Implementation

Implemented the complete normalized PostgreSQL OLTP database based on the approved enterprise architecture.

Completed business modules:

* Customer Management
* Product Management
* Location Management
* Inventory Management
* Sales Management
* Payment Management
* Returns Management
* Procurement Management

Implemented a total of **15 normalized tables** following Third Normal Form (3NF).

---

### Database Constraints

Reviewed and implemented database integrity rules.

Implemented:

* Primary Keys
* Unique Constraints
* Check Constraints
* Foreign Key Constraints

Verified referential integrity across all business entities.

---

### Performance Optimization

Designed and implemented an indexing strategy for the OLTP database.

Indexes were created on:

* Foreign key columns
* Frequently searched fields
* Business status columns
* Date columns used in reporting
* Customer lookup fields
* Product lookup fields

The indexing strategy was designed to improve transactional query performance while avoiding unnecessary indexes.

---

### Audit Automation

Implemented a reusable PostgreSQL trigger function to automatically maintain audit timestamps.

Created:

* `update_updated_at()` trigger function

Applied triggers to all tables containing an `updated_at` column to automatically update the timestamp whenever a record is modified.

---

### Deployment Preparation

Prepared a master deployment script (`run_schema.sql`) to define the correct execution order of the database components for future automated deployments using PostgreSQL's `psql` utility.

---

## Key Decisions

* Maintain a fully normalized (3NF) OLTP schema.
* Store foreign keys separately from table definitions.
* Use PostgreSQL `ENUM` types for controlled business values.
* Create performance indexes only on appropriate search, join, filter, and reporting columns.
* Centralize audit timestamp management using a reusable trigger function.
* Prepare a master deployment script for future automation while continuing manual execution in pgAdmin during development.

---

## Outcome

The RetailNova OLTP database reached a production-ready state.

Completed components:

* PostgreSQL schema
* 15 normalized tables
* ENUM types
* Primary, Unique, Check, and Foreign Key constraints
* Performance indexes
* Audit function
* Automatic update triggers

The project is now ready to begin enterprise seed data generation, which will serve as the foundation for ETL pipelines, the analytical data warehouse, SQL analytics, Power BI dashboards, and machine learning.

Day 6 — Synthetic Data Engine Foundation

Date: Day 6

Agenda
Enterprise data generation strategy
Synthetic Data Engine architecture
Historical simulation planning
Business rules
Probability models
Development environment
Product catalog strategy
Discussion
Data Generation Strategy

Reviewed multiple approaches for populating the OLTP database.

Compared:

Manual SQL INSERT statements
SQL data generation
Python-based synthetic data generation

Approved a dedicated Python-based Synthetic Data Generation Engine.

The engine will generate CSV datasets for bulk loading into PostgreSQL.

Historical Simulation

Determined that the synthetic data should simulate approximately three years of business operations.

Simulation period:

2023-01-01
2025-12-31

This enables future trend analysis, forecasting, KPI evaluation, and machine learning.

Dataset Scale

Defined realistic dataset sizes based on the RetailNova business profile.

Planned scale:

Products: ~5,000
Customers: ~50,000
Addresses: ~70,000
Memberships: ~10,000
Inventory Records: ~40,000
Orders: ~500,000
Order Items: ~1,500,000
Payments: ~500,000
Returns: ~60,000
Purchase Orders: ~8,000
Purchase Order Items: ~40,000

The scale was selected to balance realism with practical execution on a personal development machine.

Synthetic Data Engine

Designed the modular architecture for the data generation engine.

Core components include:

Configuration
Constants
Business Rules
Probability Models
Utility Functions
Dataset Generators

The engine will generate datasets in dependency order while maintaining referential integrity.

Business Simulation

Established the core simulation philosophy.

RetailNova will generate realistic enterprise data using:

Business Rules
Probability Models
Controlled Randomness

Random values alone are not acceptable.

Every generated record must represent plausible retail business behaviour.

Development Environment

Selected Google Colab as the primary development environment for rapid implementation.

The notebook will be organised into logical sections representing the planned Python modules.

After development, the notebook will be modularised into standalone Python files for the GitHub repository.

Product Catalog Strategy

Approved the use of a Product Catalog as master data.

Instead of hardcoding products within Python, the Product Generator will consume a structured product_catalog.csv.

This catalog will contain curated base products that will later be expanded into approximately 5,000 realistic SKUs through variants such as storage, colour, size, capacity, and pack size.

Key Decisions
Replace SQL INSERT scripts with a Python-based Synthetic Data Generation Engine.
Generate CSV datasets for PostgreSQL bulk loading.
Simulate three years of historical business operations.
Adopt realistic enterprise dataset sizes.
Separate business rules from probability models.
Use Google Colab for rapid development.
Treat the Product Catalog as master data rather than embedding products in code.
Outcome

Completed the foundation of the RetailNova Synthetic Data Generation Engine.

Completed components:

Configuration
Constants
Business Rules
Probability Models
Shared Utility Functions

The project is now ready to build the Product Catalog and implement the Product Generator, marking the beginning of operational data generation.

Upcoming Session
Sprint 4 — Product Master & Synthetic Data Generation

Topics:

Product Catalog creation
Product Generator implementation
Customer Generator
Inventory Generator
Procurement Generator
Order Generator
Payment Generator
Return Generator
Dataset validation
CSV export
PostgreSQL bulk loading preparation
