/*
===============================================================================
RetailNova Decision Intelligence Platform

File        : 00_types.sql
Description : Common ENUM types used throughout the RetailNova database.

Author      : Hardik Narigra
Created     : July 2026
===============================================================================
*/

-- ============================================================================
-- Customer Gender
-- ============================================================================

CREATE TYPE gender_type AS ENUM (
    'MALE',
    'FEMALE',
    'OTHER'
);

-- ============================================================================
-- Membership Status
-- ============================================================================

CREATE TYPE membership_status_type AS ENUM (
    'ACTIVE',
    'EXPIRED',
    'CANCELLED'
);

-- ============================================================================
-- Location Type
-- ============================================================================

CREATE TYPE location_type AS ENUM (
    'STORE',
    'WAREHOUSE'
);

-- ============================================================================
-- Sales Channel
-- ============================================================================

CREATE TYPE sales_channel_type AS ENUM (
    'STORE',
    'WEBSITE',
    'MOBILE_APP',
    'MARKETPLACE'
);

-- ============================================================================
-- Payment Status
-- ============================================================================

CREATE TYPE payment_status_type AS ENUM (
    'PENDING',
    'SUCCESS',
    'FAILED',
    'REFUNDED'
);

-- ============================================================================
-- Return Status
-- ============================================================================

CREATE TYPE return_status_type AS ENUM (
    'REQUESTED',
    'APPROVED',
    'REJECTED',
    'COMPLETED'
);

-- ============================================================================
-- Order Status
-- ============================================================================

CREATE TYPE order_status_type AS ENUM (
    'PENDING',
    'CONFIRMED',
    'SHIPPED',
    'DELIVERED',
    'CANCELLED'
);

-- ============================================================================
-- Purchase Order Status
-- ============================================================================

CREATE TYPE purchase_order_status_type AS ENUM (
    'CREATED',
    'APPROVED',
    'RECEIVED',
    'CANCELLED'
);
