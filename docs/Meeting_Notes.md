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

# Upcoming Session

## Sprint 2

Database Engineering

Topics:

* OLTP Database Design
* Entity Normalization
* ER Diagram
* PostgreSQL Schema
* Warehouse Mapping
* ETL Planning

---


