"""
RetailNova Decision Intelligence Platform
Synthetic Data Engine Constants

This module contains standardized business values used throughout
the RetailNova synthetic-data generation pipeline.

Author: Hardik Narigra
"""

from typing import Final, Tuple


# =========================================================
# COMPANY INFORMATION
# =========================================================

COMPANY_NAME: Final[str] = "RetailNova"
COMPANY_COUNTRY: Final[str] = "India"
COMPANY_CURRENCY: Final[str] = "INR"
COMPANY_TIMEZONE: Final[str] = "Asia/Kolkata"


# =========================================================
# CUSTOMER CONSTANTS
# =========================================================

CUSTOMER_GENDERS: Final[Tuple[str, ...]] = (
    "MALE",
    "FEMALE",
    "OTHER",
)

CUSTOMER_SEGMENTS: Final[Tuple[str, ...]] = (
    "STUDENT",
    "WORKING_PROFESSIONAL",
    "FAMILY",
    "SENIOR_CITIZEN",
    "SMALL_BUSINESS",
    "PREMIUM_MEMBER",
)

CUSTOMER_STATUSES: Final[Tuple[str, ...]] = (
    "ACTIVE",
    "INACTIVE",
    "BLOCKED",
)

ADDRESS_TYPES: Final[Tuple[str, ...]] = (
    "HOME",
    "WORK",
    "OTHER",
)


# =========================================================
# MEMBERSHIP CONSTANTS
# =========================================================

MEMBERSHIP_PLAN_NAME: Final[str] = "NovaPremium"

MEMBERSHIP_BILLING_CYCLES: Final[Tuple[str, ...]] = (
    "MONTHLY",
    "YEARLY",
)

MEMBERSHIP_STATUSES: Final[Tuple[str, ...]] = (
    "ACTIVE",
    "EXPIRED",
    "CANCELLED",
)

MONTHLY_MEMBERSHIP_FEE: Final[float] = 149.00
YEARLY_MEMBERSHIP_FEE: Final[float] = 1499.00

MONTHLY_MEMBERSHIP_DURATION_DAYS: Final[int] = 30
YEARLY_MEMBERSHIP_DURATION_DAYS: Final[int] = 365


# =========================================================
# PRODUCT CONSTANTS
# =========================================================

PRODUCT_CATEGORIES: Final[Tuple[str, ...]] = (
    "Electronics",
    "Fashion",
    "Home & Kitchen",
    "Beauty & Personal Care",
    "Sports & Fitness",
    "Books",
    "Furniture",
    "Toys & Games",
    "Grocery",
    "Smart Home",
    "Mobiles & Accessories",
    "Computers & Laptops",
    "Appliances",
    "Automotive",
    "Office Supplies",
)

PRODUCT_STATUSES: Final[Tuple[str, ...]] = (
    "ACTIVE",
    "INACTIVE",
    "DISCONTINUED",
)

PRODUCT_UNITS: Final[Tuple[str, ...]] = (
    "PIECE",
    "PACK",
    "SET",
    "PAIR",
    "BOX",
    "KG",
    "GRAM",
    "LITRE",
    "MILLILITRE",
)

GST_RATES: Final[Tuple[float, ...]] = (
    0.00,
    5.00,
    12.00,
    18.00,
    28.00,
)


# =========================================================
# SUPPLIER CONSTANTS
# =========================================================

SUPPLIER_STATUSES: Final[Tuple[str, ...]] = (
    "ACTIVE",
    "INACTIVE",
    "SUSPENDED",
)

SUPPLIER_TYPES: Final[Tuple[str, ...]] = (
    "MANUFACTURER",
    "DISTRIBUTOR",
    "WHOLESALER",
    "IMPORTER",
)


# =========================================================
# LOCATION CONSTANTS
# =========================================================

LOCATION_TYPES: Final[Tuple[str, ...]] = (
    "STORE",
    "WAREHOUSE",
)

LOCATION_STATUSES: Final[Tuple[str, ...]] = (
    "ACTIVE",
    "INACTIVE",
    "UNDER_MAINTENANCE",
)

INDIAN_STATES: Final[Tuple[str, ...]] = (
    "Maharashtra",
    "Gujarat",
    "Karnataka",
    "Tamil Nadu",
    "Telangana",
    "Delhi",
    "West Bengal",
    "Rajasthan",
    "Uttar Pradesh",
    "Madhya Pradesh",
)

INDIAN_CITIES: Final[Tuple[str, ...]] = (
    "Mumbai",
    "Pune",
    "Thane",
    "Nashik",
    "Nagpur",
    "Ahmedabad",
    "Surat",
    "Vadodara",
    "Bengaluru",
    "Mysuru",
    "Chennai",
    "Coimbatore",
    "Hyderabad",
    "New Delhi",
    "Kolkata",
    "Jaipur",
    "Lucknow",
    "Indore",
    "Bhopal",
    "Noida",
)


# =========================================================
# INVENTORY CONSTANTS
# =========================================================

INVENTORY_STATUSES: Final[Tuple[str, ...]] = (
    "IN_STOCK",
    "LOW_STOCK",
    "OUT_OF_STOCK",
    "OVERSTOCK",
)

MINIMUM_REORDER_LEVEL: Final[int] = 5
MAXIMUM_REORDER_LEVEL: Final[int] = 100

MINIMUM_REORDER_QUANTITY: Final[int] = 10
MAXIMUM_REORDER_QUANTITY: Final[int] = 500


# =========================================================
# SALES CONSTANTS
# =========================================================

SALES_CHANNELS: Final[Tuple[str, ...]] = (
    "STORE",
    "WEBSITE",
    "MOBILE_APP",
    "MARKETPLACE",
)

ORDER_STATUSES: Final[Tuple[str, ...]] = (
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
)

MINIMUM_ORDER_ITEMS: Final[int] = 1
MAXIMUM_ORDER_ITEMS: Final[int] = 8

MINIMUM_ITEM_QUANTITY: Final[int] = 1
MAXIMUM_ITEM_QUANTITY: Final[int] = 5

MINIMUM_DISCOUNT_PERCENTAGE: Final[float] = 0.00
MAXIMUM_DISCOUNT_PERCENTAGE: Final[float] = 50.00


# =========================================================
# PAYMENT CONSTANTS
# =========================================================

PAYMENT_METHODS: Final[Tuple[str, ...]] = (
    "UPI",
    "CREDIT_CARD",
    "DEBIT_CARD",
    "NET_BANKING",
    "WALLET",
    "CASH",
    "CASH_ON_DELIVERY",
)

PAYMENT_STATUSES: Final[Tuple[str, ...]] = (
    "SUCCESS",
    "FAILED",
    "PENDING",
    "REFUNDED",
)


# =========================================================
# RETURN CONSTANTS
# =========================================================

RETURN_STATUSES: Final[Tuple[str, ...]] = (
    "REQUESTED",
    "APPROVED",
    "REJECTED",
    "REFUNDED",
)

RETURN_REASONS: Final[Tuple[str, ...]] = (
    "DAMAGED_PRODUCT",
    "DEFECTIVE_PRODUCT",
    "WRONG_PRODUCT",
    "SIZE_OR_FIT_ISSUE",
    "QUALITY_NOT_AS_EXPECTED",
    "PRODUCT_NOT_REQUIRED",
    "MISSING_PARTS",
    "DELIVERED_LATE",
)

RETURN_CONDITIONS: Final[Tuple[str, ...]] = (
    "UNOPENED",
    "OPENED",
    "DAMAGED",
    "DEFECTIVE",
)


# =========================================================
# PROCUREMENT CONSTANTS
# =========================================================

PURCHASE_ORDER_STATUSES: Final[Tuple[str, ...]] = (
    "PENDING",
    "RECEIVED",
    "CANCELLED",
)

MINIMUM_SUPPLIER_LEAD_TIME_DAYS: Final[int] = 2
MAXIMUM_SUPPLIER_LEAD_TIME_DAYS: Final[int] = 30

MINIMUM_PURCHASE_ORDER_ITEMS: Final[int] = 1
MAXIMUM_PURCHASE_ORDER_ITEMS: Final[int] = 15

MINIMUM_PURCHASE_QUANTITY: Final[int] = 10
MAXIMUM_PURCHASE_QUANTITY: Final[int] = 1_000


# =========================================================
# IDENTIFIER PREFIXES
# =========================================================

IDENTIFIER_PREFIXES: Final[dict[str, str]] = {
    "customer": "CUS",
    "address": "ADR",
    "membership": "MEM",
    "category": "CAT",
    "brand": "BRD",
    "supplier": "SUP",
    "product": "PRD",
    "location": "LOC",
    "inventory": "INV",
    "order": "ORD",
    "order_item": "ORI",
    "payment": "PAY",
    "return": "RET",
    "purchase_order": "PUR",
    "purchase_order_item": "PUI",
}


# =========================================================
# CSV FILE NAMES
# =========================================================

CSV_FILE_NAMES: Final[dict[str, str]] = {
    "customer": "customer.csv",
    "address": "address.csv",
    "membership": "membership.csv",
    "category": "category.csv",
    "brand": "brand.csv",
    "supplier": "supplier.csv",
    "product": "product.csv",
    "location": "location.csv",
    "inventory": "inventory.csv",
    "orders": "orders.csv",
    "order_item": "order_item.csv",
    "payment": "payment.csv",
    "return": "return.csv",
    "purchase_order": "purchase_order.csv",
    "purchase_order_item": "purchase_order_item.csv",
}


# =========================================================
# DATE AND TIMESTAMP FORMATS
# =========================================================

DATE_FORMAT: Final[str] = "%Y-%m-%d"
TIMESTAMP_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"


# =========================================================
# VALIDATION
# =========================================================

def validate_constants() -> None:
    """
    Validate important constant collections.

    Raises
    ------
    ValueError
        If duplicate or invalid constant values are detected.
    """

    collections_to_validate = {
        "CUSTOMER_GENDERS": CUSTOMER_GENDERS,
        "CUSTOMER_SEGMENTS": CUSTOMER_SEGMENTS,
        "CUSTOMER_STATUSES": CUSTOMER_STATUSES,
        "ADDRESS_TYPES": ADDRESS_TYPES,
        "MEMBERSHIP_BILLING_CYCLES": MEMBERSHIP_BILLING_CYCLES,
        "MEMBERSHIP_STATUSES": MEMBERSHIP_STATUSES,
        "PRODUCT_CATEGORIES": PRODUCT_CATEGORIES,
        "PRODUCT_STATUSES": PRODUCT_STATUSES,
        "SUPPLIER_STATUSES": SUPPLIER_STATUSES,
        "LOCATION_TYPES": LOCATION_TYPES,
        "LOCATION_STATUSES": LOCATION_STATUSES,
        "INVENTORY_STATUSES": INVENTORY_STATUSES,
        "SALES_CHANNELS": SALES_CHANNELS,
        "ORDER_STATUSES": ORDER_STATUSES,
        "PAYMENT_METHODS": PAYMENT_METHODS,
        "PAYMENT_STATUSES": PAYMENT_STATUSES,
        "RETURN_STATUSES": RETURN_STATUSES,
        "RETURN_REASONS": RETURN_REASONS,
        "PURCHASE_ORDER_STATUSES": PURCHASE_ORDER_STATUSES,
    }

    for collection_name, values in collections_to_validate.items():
        if not values:
            raise ValueError(f"{collection_name} cannot be empty.")

        if len(values) != len(set(values)):
            raise ValueError(
                f"{collection_name} contains duplicate values."
            )

    if MONTHLY_MEMBERSHIP_FEE <= 0:
        raise ValueError("MONTHLY_MEMBERSHIP_FEE must be positive.")

    if YEARLY_MEMBERSHIP_FEE <= 0:
        raise ValueError("YEARLY_MEMBERSHIP_FEE must be positive.")

    if MINIMUM_ORDER_ITEMS > MAXIMUM_ORDER_ITEMS:
        raise ValueError(
            "MINIMUM_ORDER_ITEMS cannot exceed MAXIMUM_ORDER_ITEMS."
        )

    if MINIMUM_ITEM_QUANTITY > MAXIMUM_ITEM_QUANTITY:
        raise ValueError(
            "MINIMUM_ITEM_QUANTITY cannot exceed MAXIMUM_ITEM_QUANTITY."
        )

    if MINIMUM_DISCOUNT_PERCENTAGE > MAXIMUM_DISCOUNT_PERCENTAGE:
        raise ValueError(
            "Minimum discount cannot exceed maximum discount."
        )

    expected_csv_count = 15

    if len(CSV_FILE_NAMES) != expected_csv_count:
        raise ValueError(
            f"Expected {expected_csv_count} CSV file mappings, "
            f"found {len(CSV_FILE_NAMES)}."
        )


validate_constants()


if __name__ == "__main__":
    print("RetailNova constants validated successfully.")
    print(f"Product categories: {len(PRODUCT_CATEGORIES)}")
    print(f"Customer segments: {len(CUSTOMER_SEGMENTS)}")
    print(f"Sales channels: {len(SALES_CHANNELS)}")
    print(f"Payment methods: {len(PAYMENT_METHODS)}")
    print(f"Required CSV files: {len(CSV_FILE_NAMES)}")

constants_path = (
    "/content/retailnova/python/generators/constants.py"
)

replace_required(
    constants_path,
    '''ORDER_STATUSES: Final[Tuple[str, ...]] = (
    "PLACED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
)''',
    '''ORDER_STATUSES: Final[Tuple[str, ...]] = (
    "PENDING",
    "CONFIRMED",
    "SHIPPED",
    "DELIVERED",
    "CANCELLED",
)''',
)

replace_required(
    constants_path,
    '''RETURN_STATUSES: Final[Tuple[str, ...]] = (
    "REQUESTED",
    "APPROVED",
    "REJECTED",
    "REFUNDED",
)''',
    '''RETURN_STATUSES: Final[Tuple[str, ...]] = (
    "REQUESTED",
    "APPROVED",
    "REJECTED",
    "COMPLETED",
)''',
)

replace_required(
    constants_path,
    '''PURCHASE_ORDER_STATUSES: Final[Tuple[str, ...]] = (
    "PENDING",
    "RECEIVED",
    "CANCELLED",
)''',
    '''PURCHASE_ORDER_STATUSES: Final[Tuple[str, ...]] = (
    "CREATED",
    "APPROVED",
    "RECEIVED",
    "CANCELLED",
)''',
)
