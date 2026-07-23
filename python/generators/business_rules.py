%%writefile /content/retailnova/python/generators/business_rules.py

"""
RetailNova Decision Intelligence Platform
Synthetic Data Engine Business Rules

This module contains deterministic retail business rules used by
the synthetic-data generators.

Probabilistic behaviour belongs in probability_models.py.

Author: Hardik Narigra
"""

from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Final, Union

try:
    from .constants import (
        MAXIMUM_DISCOUNT_PERCENTAGE,
        MEMBERSHIP_BILLING_CYCLES,
        MONTHLY_MEMBERSHIP_DURATION_DAYS,
        MONTHLY_MEMBERSHIP_FEE,
        ORDER_STATUSES,
        PAYMENT_STATUSES,
        PURCHASE_ORDER_STATUSES,
        RETURN_STATUSES,
        YEARLY_MEMBERSHIP_DURATION_DAYS,
        YEARLY_MEMBERSHIP_FEE,
    )
except ImportError:
    from constants import (
        MAXIMUM_DISCOUNT_PERCENTAGE,
        MEMBERSHIP_BILLING_CYCLES,
        MONTHLY_MEMBERSHIP_DURATION_DAYS,
        MONTHLY_MEMBERSHIP_FEE,
        ORDER_STATUSES,
        PAYMENT_STATUSES,
        PURCHASE_ORDER_STATUSES,
        RETURN_STATUSES,
        YEARLY_MEMBERSHIP_DURATION_DAYS,
        YEARLY_MEMBERSHIP_FEE,
    )


Number = Union[int, float, Decimal]


# =========================================================
# GENERAL FINANCIAL RULES
# =========================================================

CURRENCY_DECIMAL_PLACES: Final[str] = "0.01"
MINIMUM_PRODUCT_MARKUP_PERCENTAGE: Final[Decimal] = Decimal("10.00")
MAXIMUM_PRODUCT_MARKUP_PERCENTAGE: Final[Decimal] = Decimal("80.00")

MINIMUM_VALID_PRODUCT_PRICE: Final[Decimal] = Decimal("1.00")
MAXIMUM_VALID_PRODUCT_PRICE: Final[Decimal] = Decimal("1000000.00")

STANDARD_RETURN_WINDOW_DAYS: Final[int] = 15
EXTENDED_PREMIUM_RETURN_WINDOW_DAYS: Final[int] = 30


# =========================================================
# CATEGORY BUSINESS RULES
# =========================================================

CATEGORY_MARGIN_RANGES: Final[dict[str, tuple[float, float]]] = {
    "Electronics": (8.00, 20.00),
    "Fashion": (25.00, 55.00),
    "Home & Kitchen": (18.00, 40.00),
    "Beauty & Personal Care": (25.00, 50.00),
    "Sports & Fitness": (20.00, 45.00),
    "Books": (15.00, 35.00),
    "Furniture": (20.00, 45.00),
    "Toys & Games": (20.00, 45.00),
    "Grocery": (5.00, 18.00),
    "Smart Home": (15.00, 35.00),
    "Mobiles & Accessories": (8.00, 30.00),
    "Computers & Laptops": (7.00, 18.00),
    "Appliances": (10.00, 25.00),
    "Automotive": (15.00, 35.00),
    "Office Supplies": (20.00, 45.00),
}

CATEGORY_GST_RATES: Final[dict[str, tuple[float, ...]]] = {
    "Electronics": (18.00, 28.00),
    "Fashion": (5.00, 12.00),
    "Home & Kitchen": (5.00, 12.00, 18.00),
    "Beauty & Personal Care": (12.00, 18.00),
    "Sports & Fitness": (12.00, 18.00),
    "Books": (0.00,),
    "Furniture": (12.00, 18.00),
    "Toys & Games": (12.00, 18.00),
    "Grocery": (0.00, 5.00, 12.00),
    "Smart Home": (18.00, 28.00),
    "Mobiles & Accessories": (18.00,),
    "Computers & Laptops": (18.00,),
    "Appliances": (18.00, 28.00),
    "Automotive": (18.00, 28.00),
    "Office Supplies": (12.00, 18.00),
}

CATEGORY_RETURN_ELIGIBILITY: Final[dict[str, bool]] = {
    "Electronics": True,
    "Fashion": True,
    "Home & Kitchen": True,
    "Beauty & Personal Care": False,
    "Sports & Fitness": True,
    "Books": True,
    "Furniture": True,
    "Toys & Games": True,
    "Grocery": False,
    "Smart Home": True,
    "Mobiles & Accessories": True,
    "Computers & Laptops": True,
    "Appliances": True,
    "Automotive": True,
    "Office Supplies": True,
}


# =========================================================
# DECIMAL AND FINANCIAL HELPERS
# =========================================================

def to_decimal(value: Number) -> Decimal:
    """Convert a numeric value safely to Decimal."""

    return Decimal(str(value))


def round_currency(value: Number) -> Decimal:
    """Round a numeric value to two currency decimal places."""

    return to_decimal(value).quantize(
        Decimal(CURRENCY_DECIMAL_PLACES),
        rounding=ROUND_HALF_UP,
    )


def calculate_selling_price(
    cost_price: Number,
    markup_percentage: Number,
) -> Decimal:
    """
    Calculate selling price from cost and markup.

    Selling price = cost price × (1 + markup percentage / 100)
    """

    cost = to_decimal(cost_price)
    markup = to_decimal(markup_percentage)

    if cost <= 0:
        raise ValueError("cost_price must be greater than zero.")

    if not (
        MINIMUM_PRODUCT_MARKUP_PERCENTAGE
        <= markup
        <= MAXIMUM_PRODUCT_MARKUP_PERCENTAGE
    ):
        raise ValueError(
            "markup_percentage must be between "
            f"{MINIMUM_PRODUCT_MARKUP_PERCENTAGE}% and "
            f"{MAXIMUM_PRODUCT_MARKUP_PERCENTAGE}%."
        )

    selling_price = cost * (Decimal("1") + markup / Decimal("100"))

    return round_currency(selling_price)


def calculate_discount_amount(
    gross_amount: Number,
    discount_percentage: Number,
) -> Decimal:
    """Calculate the discount applied to a gross amount."""

    gross = to_decimal(gross_amount)
    discount = to_decimal(discount_percentage)

    if gross < 0:
        raise ValueError("gross_amount cannot be negative.")

    if not Decimal("0") <= discount <= to_decimal(
        MAXIMUM_DISCOUNT_PERCENTAGE
    ):
        raise ValueError(
            "discount_percentage must be between 0 and "
            f"{MAXIMUM_DISCOUNT_PERCENTAGE}."
        )

    return round_currency(
        gross * discount / Decimal("100")
    )


def calculate_tax_amount(
    taxable_amount: Number,
    gst_rate: Number,
) -> Decimal:
    """Calculate GST on a taxable amount."""

    taxable = to_decimal(taxable_amount)
    rate = to_decimal(gst_rate)

    if taxable < 0:
        raise ValueError("taxable_amount cannot be negative.")

    if rate < 0:
        raise ValueError("gst_rate cannot be negative.")

    return round_currency(
        taxable * rate / Decimal("100")
    )


def calculate_order_item_totals(
    unit_price: Number,
    quantity: int,
    discount_percentage: Number,
    gst_rate: Number,
) -> dict[str, Decimal]:
    """
    Calculate all monetary values for one order item.

    GST is calculated after applying the item discount.
    """

    price = to_decimal(unit_price)

    if price <= 0:
        raise ValueError("unit_price must be greater than zero.")

    if quantity <= 0:
        raise ValueError("quantity must be greater than zero.")

    gross_amount = round_currency(price * quantity)

    discount_amount = calculate_discount_amount(
        gross_amount,
        discount_percentage,
    )

    taxable_amount = round_currency(
        gross_amount - discount_amount
    )

    tax_amount = calculate_tax_amount(
        taxable_amount,
        gst_rate,
    )

    line_total = round_currency(
        taxable_amount + tax_amount
    )

    return {
        "gross_amount": gross_amount,
        "discount_amount": discount_amount,
        "taxable_amount": taxable_amount,
        "tax_amount": tax_amount,
        "line_total": line_total,
    }


def reconcile_order_totals(
    item_totals: list[dict[str, Decimal]],
) -> dict[str, Decimal]:
    """Aggregate order-item values into order-level totals."""

    if not item_totals:
        raise ValueError(
            "At least one order item is required."
        )

    subtotal = round_currency(
        sum(
            (
                item["gross_amount"]
                for item in item_totals
            ),
            Decimal("0"),
        )
    )

    discount_amount = round_currency(
        sum(
            (
                item["discount_amount"]
                for item in item_totals
            ),
            Decimal("0"),
        )
    )

    tax_amount = round_currency(
        sum(
            (
                item["tax_amount"]
                for item in item_totals
            ),
            Decimal("0"),
        )
    )

    total_amount = round_currency(
        sum(
            (
                item["line_total"]
                for item in item_totals
            ),
            Decimal("0"),
        )
    )

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
    }


# =========================================================
# MEMBERSHIP RULES
# =========================================================

def get_membership_fee(billing_cycle: str) -> Decimal:
    """Return the approved fee for a billing cycle."""

    cycle = billing_cycle.strip().upper()

    if cycle not in MEMBERSHIP_BILLING_CYCLES:
        raise ValueError(
            f"Invalid billing cycle: {billing_cycle}"
        )

    if cycle == "MONTHLY":
        return round_currency(MONTHLY_MEMBERSHIP_FEE)

    return round_currency(YEARLY_MEMBERSHIP_FEE)


def calculate_membership_end_date(
    start_date: date,
    billing_cycle: str,
) -> date:
    """Calculate membership end date from its billing cycle."""

    if not isinstance(start_date, date):
        raise TypeError(
            "start_date must be a date object."
        )

    cycle = billing_cycle.strip().upper()

    if cycle == "MONTHLY":
        duration = MONTHLY_MEMBERSHIP_DURATION_DAYS
    elif cycle == "YEARLY":
        duration = YEARLY_MEMBERSHIP_DURATION_DAYS
    else:
        raise ValueError(
            f"Invalid billing cycle: {billing_cycle}"
        )

    return start_date + timedelta(days=duration)


# =========================================================
# INVENTORY RULES
# =========================================================

def determine_inventory_status(
    quantity_on_hand: int,
    reorder_level: int,
    maximum_stock_level: int,
) -> str:
    """Determine inventory status from stock levels."""

    if quantity_on_hand < 0:
        raise ValueError(
            "quantity_on_hand cannot be negative."
        )

    if reorder_level < 0:
        raise ValueError(
            "reorder_level cannot be negative."
        )

    if maximum_stock_level <= reorder_level:
        raise ValueError(
            "maximum_stock_level must be greater "
            "than reorder_level."
        )

    if quantity_on_hand == 0:
        return "OUT_OF_STOCK"

    if quantity_on_hand <= reorder_level:
        return "LOW_STOCK"

    if quantity_on_hand > maximum_stock_level:
        return "OVERSTOCK"

    return "IN_STOCK"


def calculate_available_quantity(
    quantity_on_hand: int,
    reserved_quantity: int,
) -> int:
    """Calculate inventory available for sale."""

    if quantity_on_hand < 0:
        raise ValueError(
            "quantity_on_hand cannot be negative."
        )

    if reserved_quantity < 0:
        raise ValueError(
            "reserved_quantity cannot be negative."
        )

    if reserved_quantity > quantity_on_hand:
        raise ValueError(
            "reserved_quantity cannot exceed "
            "quantity_on_hand."
        )

    return quantity_on_hand - reserved_quantity


# =========================================================
# ORDER AND PAYMENT RULES
# =========================================================

def validate_order_timeline(
    order_date: datetime,
    shipped_date: datetime | None,
    delivered_date: datetime | None,
    order_status: str,
) -> None:
    """Validate chronological consistency of an order."""

    status = order_status.strip().upper()

    if status not in ORDER_STATUSES:
        raise ValueError(
            f"Invalid order status: {order_status}"
        )

    if shipped_date and shipped_date < order_date:
        raise ValueError(
            "shipped_date cannot precede order_date."
        )

    if delivered_date:
        if shipped_date is None:
            raise ValueError(
                "A delivered order requires shipped_date."
            )

        if delivered_date < shipped_date:
            raise ValueError(
                "delivered_date cannot precede shipped_date."
            )

    if status == "PLACED":
        if shipped_date or delivered_date:
            raise ValueError(
                "PLACED orders cannot have shipping "
                "or delivery dates."
            )

    elif status == "SHIPPED":
        if shipped_date is None:
            raise ValueError(
                "SHIPPED orders require shipped_date."
            )

        if delivered_date is not None:
            raise ValueError(
                "SHIPPED orders cannot have delivered_date."
            )

    elif status == "DELIVERED":
        if shipped_date is None or delivered_date is None:
            raise ValueError(
                "DELIVERED orders require both dates."
            )

    elif status == "CANCELLED":
        if delivered_date is not None:
            raise ValueError(
                "CANCELLED orders cannot be delivered."
            )


def expected_payment_status(order_status: str) -> str:
    """Return the usual payment status for an order."""

    status = order_status.strip().upper()

    if status not in ORDER_STATUSES:
        raise ValueError(
            f"Invalid order status: {order_status}"
        )

    status_mapping = {
        "PLACED": "PENDING",
        "SHIPPED": "SUCCESS",
        "DELIVERED": "SUCCESS",
        "CANCELLED": "REFUNDED",
    }

    return status_mapping[status]


def validate_payment_amounts(
    order_total: Number,
    payment_amount: Number,
    payment_status: str,
) -> None:
    """Validate payment amount against the order total."""

    order_value = round_currency(order_total)
    paid_value = round_currency(payment_amount)
    status = payment_status.strip().upper()

    if status not in PAYMENT_STATUSES:
        raise ValueError(
            f"Invalid payment status: {payment_status}"
        )

    if order_value < 0 or paid_value < 0:
        raise ValueError(
            "Order and payment values cannot be negative."
        )

    if status in {"SUCCESS", "REFUNDED"}:
        if paid_value != order_value:
            raise ValueError(
                "Successful or refunded payment must equal "
                "the order total."
            )


# =========================================================
# RETURN RULES
# =========================================================

def is_return_eligible(
    category_name: str,
    delivered_date: date,
    requested_date: date,
    is_premium_member: bool = False,
) -> bool:
    """Determine whether an order item is eligible for return."""

    if requested_date < delivered_date:
        return False

    category_eligible = CATEGORY_RETURN_ELIGIBILITY.get(
        category_name,
        False,
    )

    if not category_eligible:
        return False

    return_window = (
        EXTENDED_PREMIUM_RETURN_WINDOW_DAYS
        if is_premium_member
        else STANDARD_RETURN_WINDOW_DAYS
    )

    days_since_delivery = (
        requested_date - delivered_date
    ).days

    return days_since_delivery <= return_window


def validate_return_status(
    order_status: str,
    return_status: str,
) -> None:
    """Ensure a return belongs to a delivered order."""

    normalized_order_status = order_status.strip().upper()
    normalized_return_status = return_status.strip().upper()

    if normalized_return_status not in RETURN_STATUSES:
        raise ValueError(
            f"Invalid return status: {return_status}"
        )

    if normalized_order_status != "DELIVERED":
        raise ValueError(
            "Only delivered orders are eligible for returns."
        )


# =========================================================
# PROCUREMENT RULES
# =========================================================

def calculate_expected_delivery_date(
    purchase_order_date: date,
    supplier_lead_time_days: int,
) -> date:
    """Calculate expected procurement delivery date."""

    if supplier_lead_time_days <= 0:
        raise ValueError(
            "supplier_lead_time_days must be positive."
        )

    return purchase_order_date + timedelta(
        days=supplier_lead_time_days
    )


def validate_purchase_order_dates(
    order_date: date,
    expected_delivery_date: date,
    received_date: date | None,
    purchase_order_status: str,
) -> None:
    """Validate procurement dates and status consistency."""

    status = purchase_order_status.strip().upper()

    if status not in PURCHASE_ORDER_STATUSES:
        raise ValueError(
            f"Invalid purchase order status: "
            f"{purchase_order_status}"
        )

    if expected_delivery_date < order_date:
        raise ValueError(
            "expected_delivery_date cannot precede order_date."
        )

    if received_date and received_date < order_date:
        raise ValueError(
            "received_date cannot precede order_date."
        )

    if status == "RECEIVED" and received_date is None:
        raise ValueError(
            "RECEIVED purchase orders require received_date."
        )

    if status in {"PENDING", "CANCELLED"}:
        if received_date is not None:
            raise ValueError(
                f"{status} purchase orders cannot have "
                "received_date."
            )


# =========================================================
# MODULE VALIDATION
# =========================================================

def validate_business_rules() -> None:
    """Validate all static RetailNova business rules."""

    if set(CATEGORY_MARGIN_RANGES) != set(
        CATEGORY_GST_RATES
    ):
        raise ValueError(
            "Category margin and GST mappings do not match."
        )

    if set(CATEGORY_MARGIN_RANGES) != set(
        CATEGORY_RETURN_ELIGIBILITY
    ):
        raise ValueError(
            "Category margin and return mappings do not match."
        )

    for category, margin_range in (
        CATEGORY_MARGIN_RANGES.items()
    ):
        minimum_margin, maximum_margin = margin_range

        if minimum_margin < 0:
            raise ValueError(
                f"{category} has a negative minimum margin."
            )

        if minimum_margin > maximum_margin:
            raise ValueError(
                f"{category} has an invalid margin range."
            )

    for category, rates in CATEGORY_GST_RATES.items():
        if not rates:
            raise ValueError(
                f"{category} has no GST rate."
            )

        if any(rate < 0 for rate in rates):
            raise ValueError(
                f"{category} contains a negative GST rate."
            )


validate_business_rules()


if __name__ == "__main__":
    print("RetailNova business rules validated.")
    print(
        "Configured categories:",
        len(CATEGORY_MARGIN_RANGES),
    )
