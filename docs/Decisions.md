# RetailNova Decision Log

## Purpose

This document records all major architectural, technical, and business decisions made throughout the RetailNova Decision Intelligence Platform project.

Each decision includes the rationale, alternatives considered, and implementation status to maintain project transparency and architectural consistency.

---

# DEC-001

## Date

Day 1

## Decision

Select the Retail Industry as the project domain.

## Reason

Retail provides rich business processes including sales, inventory, procurement, logistics, marketing, finance, and customer analytics. It enables implementation of SQL analytics, Machine Learning, Business Intelligence, and AI decision support within a single enterprise platform.

## Alternatives Considered

* Banking
* Healthcare
* Manufacturing
* Education

## Status

Approved

---

# DEC-002

## Date

Day 1

## Decision

Build an Enterprise Decision Intelligence Platform instead of a traditional dashboard project.

## Reason

The objective is to solve enterprise business problems using data engineering, analytics, machine learning, and AI rather than building isolated visualizations.

## Alternatives Considered

* Sales Dashboard
* HR Dashboard
* Inventory Dashboard
* E-commerce Dashboard

## Status

Approved

---

# DEC-003

## Date

Day 1

## Decision

Use PostgreSQL as the primary relational database.

## Reason

PostgreSQL is enterprise-grade, open-source, highly reliable, supports advanced SQL features, and integrates well with analytics tools.

## Alternatives Considered

* MySQL
* SQL Server
* SQLite

## Status

Approved

---

# DEC-004

## Date

Day 1

## Decision

Use Python as the primary analytics language.

## Reason

Python supports data engineering, analytics, visualization, machine learning, forecasting, and AI development using a single ecosystem.

## Alternatives Considered

* R
* Java
* Scala

## Status

Approved

---

# DEC-005

## Date

Day 1

## Decision

Use Power BI for Business Intelligence.

## Reason

Power BI provides enterprise dashboarding, KPI monitoring, executive reporting, and seamless integration with SQL databases.

## Alternatives Considered

* Tableau
* Looker
* Apache Superset

## Status

Approved

---

# DEC-006

## Date

Day 1

## Decision

Use Streamlit as the application framework.

## Reason

Streamlit enables rapid development of interactive analytics applications and AI-assisted decision support interfaces.

## Alternatives Considered

* Flask
* Django
* React

## Status

Approved

---

# DEC-007

## Date

Day 1

## Decision

Use a synthetic enterprise dataset.

## Reason

No publicly available dataset represents the complete RetailNova business model or supports all planned analytical use cases.

## Alternatives Considered

* Kaggle datasets
* Public retail datasets
* Sample ERP databases

## Status

Approved

---

# DEC-008

## Date

Day 1

## Decision

Adopt a Business-First Development methodology.

## Reason

Every technical implementation must directly support a documented business requirement and business question.

## Alternatives Considered

Feature-first development.

## Status

Approved

---

# DEC-009

## Date

Day 1

## Decision

Develop an AI-assisted Decision Support Engine.

## Reason

The objective is to generate business recommendations rather than only descriptive analytics.

## Alternatives Considered

Traditional reporting only.

## Status

Approved

---

# DEC-010

## Date

Day 1

## Decision

Maintain documentation before implementation.

## Reason

Enterprise software should be architecture-driven. Documentation reduces ambiguity and supports long-term maintainability.

## Alternatives Considered

Code-first development.

## Status

Approved

---

# DEC-011

## Date

Day 3

## Decision

Adopt Dual Logical Architecture (OLTP + OLAP).

## Reason

Separate operational transaction processing from analytical workloads to improve scalability, reporting performance, and architectural clarity.

## Alternatives Considered

Single database architecture.

## Status

Approved

---

# DEC-012

## Date

Day 3

## Decision

Use Kimball Dimensional Modeling for the Enterprise Data Warehouse.

## Reason

Kimball provides excellent support for SQL analytics, Power BI dashboards, Machine Learning feature engineering, and AI decision support through dimensional modeling.

## Alternatives Considered

* Inmon Enterprise Data Warehouse
* Data Vault

## Status

Approved

---

# DEC-013

## Date

Day 3

## Decision

Implement Multiple Star Schemas using Kimball Bus Architecture.

## Reason

Each major business process owns an independent analytical model while sharing conformed dimensions across the enterprise.

## Alternatives Considered

* Single enterprise fact table
* Snowflake-only architecture

## Status

Approved

---

# DEC-014

## Date

Day 3

## Decision

Generate synthetic enterprise data instead of relying entirely on public datasets.

## Reason

RetailNova requires complete control over business processes, historical events, and analytical scenarios that public datasets cannot provide.

## Alternatives Considered

* Kaggle datasets
* Public retail transaction datasets

## Status

Approved

---

# DEC-015

## Date

Day 3

## Decision

Adopt a Hybrid Enterprise Data Generation Strategy.

## Reason

Realistic enterprise data requires a combination of business rules, probability distributions, and controlled randomness rather than purely random value generation.

## Alternatives Considered

* Random data generation
* Pure rule-based simulation
* Pure probabilistic simulation

## Status

Approved

---

# DEC-016

## Date

Day 3

## Decision

Design the warehouse using subject-oriented business domains.

## Reason

Separating Sales, Inventory, Procurement, Marketing, and Returns into distinct analytical domains improves scalability, maintainability, and ownership while sharing conformed dimensions.

## Alternatives Considered

Single monolithic warehouse model.

## Status

Approved

---

# DEC-017

## Date

Day 3

## Decision

Implement the project incrementally using development sprints.

## Reason

The project scope is enterprise-scale. Delivering functionality through incremental sprints reduces complexity, improves testing, and ensures continuous progress.

## Alternatives Considered

Complete all documentation followed by one large implementation phase.

## Status

Approved

---

---

# DEC-018

## Date

Day 4

## Decision

Merge Store and Warehouse into a unified Location entity.

## Reason

Stores and warehouses share nearly identical attributes and differ primarily by their operational role. A single Location table with a `location_type` attribute simplifies the schema, reduces redundancy, and enables cleaner inventory and order relationships.

## Alternatives Considered

* Separate Store and Warehouse tables
* Generic Location entity

## Status

Approved

---

# DEC-019

## Date

Day 4

## Decision

Implement a single Membership model without a MembershipPlan table.

## Reason

RetailNova offers only one Premium membership with two billing cycles (Monthly and Yearly). Creating a separate MembershipPlan table would add unnecessary complexity without business value.

## Alternatives Considered

* MembershipPlan table
* Multiple membership tiers

## Status

Approved

---

# DEC-020

## Date

Day 4

## Decision

Track only current inventory and exclude InventoryMovement from Version 1.

## Reason

The primary objective is business analytics rather than warehouse operations. Current inventory levels are sufficient for dashboards, forecasting, and AI recommendations.

## Alternatives Considered

* Inventory table only
* Inventory + InventoryMovement tables

## Status

Approved

---

# DEC-021

## Date

Day 4

## Decision

Reference OrderItem directly in the Return table.

## Reason

Each returned product should be linked to the exact purchased item. This eliminates the need for a separate ReturnItem table while supporting product-level return analytics.

## Alternatives Considered

* Return + ReturnItem
* Return referencing Order only

## Status

Approved

---

# DEC-022

## Date

Day 4

## Decision

Allow only one payment per order.

## Reason

Version 1 does not support split payments or partial payments. Restricting each order to a single payment simplifies the payment model while satisfying all business requirements.

## Alternatives Considered

* Multiple payments per order
* Partial payment support

## Status

Approved

---

# DEC-023

## Date

Day 4

## Decision

Assign a single primary supplier to each product.

## Reason

A one-to-many relationship between Supplier and Product simplifies procurement, inventory management, and analytics while avoiding unnecessary bridge tables.

## Alternatives Considered

* Many-to-many Product-Supplier relationship

## Status

Approved

---

# DEC-024

## Date

Day 4

## Decision

Capture the sales channel for every order.

## Reason

RetailNova operates across multiple channels. Recording the order source enables channel-wise sales analysis, customer behavior analysis, and AI-driven business insights.

## Supported Sales Channels

* STORE
* WEBSITE
* MOBILE_APP
* MARKETPLACE

## Alternatives Considered

* Store sales only
* Online/Offline flag only

## Status

Approved

---

# DEC-025

## Date

Day 4

## Decision

Design the operational database in Third Normal Form (3NF).

## Reason

Normalization minimizes redundancy, improves data integrity, and provides a clean operational database that serves as the source system for the enterprise data warehouse.

## Alternatives Considered

* Partially normalized schema
* Denormalized operational database

## Status

Approved

---

# DEC-026

## Date

Day 4

## Decision

Limit the operational database to 15 core business tables.

## Reason

Every table must have clear operational and analytical value. Additional entities such as InventoryMovement, ShoppingCart, Wishlist, Employee, Coupons, and Loyalty Points are intentionally deferred to future releases to maintain simplicity and focus.

## Alternatives Considered

* Expanded ERP-style schema
* Minimal e-commerce schema

## Status

Approved
