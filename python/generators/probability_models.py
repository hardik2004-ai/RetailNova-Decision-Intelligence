%%writefile /content/retailnova/python/generators/probability_models.py

"""
RetailNova Decision Intelligence Platform
Synthetic Data Engine Probability Models

This module defines weighted probability distributions and
seasonal behaviour used by RetailNova data generators.

Author: Hardik Narigra
"""

import random
from datetime import date, datetime
from typing import Mapping, Sequence, TypeVar

try:
    from .constants import (
        ADDRESS_TYPES,
        CUSTOMER_GENDERS,
        CUSTOMER_SEGMENTS,
        CUSTOMER_STATUSES,
        LOCATION_STATUSES,
        MEMBERSHIP_BILLING_CYCLES,
        MEMBERSHIP_STATUSES,
        ORDER_STATUSES,
        PAYMENT_METHODS,
        PAYMENT_STATUSES,
        PRODUCT_STATUSES,
        PURCHASE_ORDER_STATUSES,
        RETURN_REASONS,
        RETURN_STATUSES,
        SALES_CHANNELS,
        SUPPLIER_STATUSES,
    )
except ImportError:
    from constants import (
        ADDRESS_TYPES,
        CUSTOMER_GENDERS,
        CUSTOMER_SEGMENTS,
        CUSTOMER_STATUSES,
        LOCATION_STATUSES,
        MEMBERSHIP_BILLING_CYCLES,
        MEMBERSHIP_STATUSES,
        ORDER_STATUSES,
        PAYMENT_METHODS,
        PAYMENT_STATUSES,
        PRODUCT_STATUSES,
        PURCHASE_ORDER_STATUSES,
        RETURN_REASONS,
        RETURN_STATUSES,
        SALES_CHANNELS,
        SUPPLIER_STATUSES,
    )


T = TypeVar("T")


# =========================================================
# WEIGHTED DISTRIBUTIONS
# =========================================================

CUSTOMER_GENDER_WEIGHTS = {
    "MALE": 0.50,
    "FEMALE": 0.48,
    "OTHER": 0.02,
}

CUSTOMER_SEGMENT_WEIGHTS = {
    "STUDENT": 0.14,
    "WORKING_PROFESSIONAL": 0.32,
    "FAMILY": 0.27,
    "SENIOR_CITIZEN": 0.09,
    "SMALL_BUSINESS": 0.08,
    "PREMIUM_MEMBER": 0.10,
}

CUSTOMER_STATUS_WEIGHTS = {
    "ACTIVE": 0.93,
    "INACTIVE": 0.06,
    "BLOCKED": 0.01,
}

ADDRESS_TYPE_WEIGHTS = {
    "HOME": 0.76,
    "WORK": 0.19,
    "OTHER": 0.05,
}

MEMBERSHIP_BILLING_CYCLE_WEIGHTS = {
    "MONTHLY": 0.68,
    "YEARLY": 0.32,
}

MEMBERSHIP_STATUS_WEIGHTS = {
    "ACTIVE": 0.72,
    "EXPIRED": 0.22,
    "CANCELLED": 0.06,
}

PRODUCT_STATUS_WEIGHTS = {
    "ACTIVE": 0.94,
    "INACTIVE": 0.04,
    "DISCONTINUED": 0.02,
}

SUPPLIER_STATUS_WEIGHTS = {
    "ACTIVE": 0.90,
    "INACTIVE": 0.07,
    "SUSPENDED": 0.03,
}

LOCATION_STATUS_WEIGHTS = {
    "ACTIVE": 0.94,
    "INACTIVE": 0.03,
    "UNDER_MAINTENANCE": 0.03,
}

SALES_CHANNEL_WEIGHTS = {
    "STORE": 0.34,
    "WEBSITE": 0.27,
    "MOBILE_APP": 0.29,
    "MARKETPLACE": 0.10,
}

ORDER_STATUS_WEIGHTS = {
    "PLACED": 0.04,
    "SHIPPED": 0.06,
    "DELIVERED": 0.86,
    "CANCELLED": 0.04,
}

PAYMENT_METHOD_WEIGHTS = {
    "UPI": 0.36,
    "CREDIT_CARD": 0.18,
    "DEBIT_CARD": 0.14,
    "NET_BANKING": 0.08,
    "WALLET": 0.08,
    "CASH": 0.10,
    "CASH_ON_DELIVERY": 0.06,
}

PAYMENT_STATUS_WEIGHTS = {
    "SUCCESS": 0.93,
    "FAILED": 0.025,
    "PENDING": 0.025,
    "REFUNDED": 0.02,
}

RETURN_STATUS_WEIGHTS = {
    "REQUESTED": 0.12,
    "APPROVED": 0.23,
    "REJECTED": 0.10,
    "REFUNDED": 0.55,
}

RETURN_REASON_WEIGHTS = {
    "DAMAGED_PRODUCT": 0.16,
    "DEFECTIVE_PRODUCT": 0.18,
    "WRONG_PRODUCT": 0.10,
    "SIZE_OR_FIT_ISSUE": 0.20,
    "QUALITY_NOT_AS_EXPECTED": 0.15,
    "PRODUCT_NOT_REQUIRED": 0.09,
    "MISSING_PARTS": 0.07,
    "DELIVERED_LATE": 0.05,
}

PURCHASE_ORDER_STATUS_WEIGHTS = {
    "PENDING": 0.12,
    "RECEIVED": 0.84,
    "CANCELLED": 0.04,
}

ORDER_ITEM_COUNT_WEIGHTS = {
    1: 0.34,
    2: 0.28,
    3: 0.18,
    4: 0.10,
    5: 0.05,
    6: 0.025,
    7: 0.015,
    8: 0.01,
}

ITEM_QUANTITY_WEIGHTS = {
    1: 0.70,
    2: 0.19,
    3: 0.07,
    4: 0.025,
    5: 0.015,
}

DISCOUNT_PERCENTAGE_WEIGHTS = {
    0.0: 0.38,
    5.0: 0.17,
    10.0: 0.19,
    15.0: 0.11,
    20.0: 0.08,
    25.0: 0.04,
    30.0: 0.02,
    40.0: 0.007,
    50.0: 0.003,
}


# =========================================================
# SEASONAL DEMAND
# =========================================================

MONTHLY_DEMAND_MULTIPLIERS = {
    1: 0.93,
    2: 0.88,
    3: 0.96,
    4: 1.00,
    5: 1.04,
    6: 0.95,
    7: 0.98,
    8: 1.05,
    9: 1.12,
    10: 1.35,
    11: 1.42,
    12: 1.30,
}

WEEKDAY_DEMAND_MULTIPLIERS = {
    0: 0.90,  # Monday
    1: 0.92,
    2: 0.95,
    3: 0.98,
    4: 1.08,
    5: 1.22,
    6: 1.18,  # Sunday
}

FESTIVAL_DEMAND_MULTIPLIERS = {
    (1, 26): 1.25,
    (8, 15): 1.20,
    (10, 2): 1.18,
    (12, 25): 1.30,
}

FESTIVAL_SEASONS = {
    1: 1.05,
    8: 1.08,
    9: 1.12,
    10: 1.28,
    11: 1.30,
    12: 1.18,
}


# =========================================================
# PROBABILITY UTILITIES
# =========================================================

def validate_distribution(
    distribution: Mapping[T, float],
    distribution_name: str = "distribution",
    tolerance: float = 1e-9,
) -> None:
    """Validate a weighted probability distribution."""

    if not distribution:
        raise ValueError(
            f"{distribution_name} cannot be empty."
        )

    if any(weight < 0 for weight in distribution.values()):
        raise ValueError(
            f"{distribution_name} contains negative weights."
        )

    total = sum(distribution.values())

    if abs(total - 1.0) > tolerance:
        raise ValueError(
            f"{distribution_name} weights must total 1.0; "
            f"found {total:.12f}."
        )


def weighted_choice(
    distribution: Mapping[T, float],
    rng: random.Random | None = None,
) -> T:
    """Return one value using the supplied weighted distribution."""

    validate_distribution(distribution)

    random_generator = rng or random

    values = list(distribution.keys())
    weights = list(distribution.values())

    return random_generator.choices(
        population=values,
        weights=weights,
        k=1,
    )[0]


def weighted_choices(
    distribution: Mapping[T, float],
    count: int,
    rng: random.Random | None = None,
) -> list[T]:
    """Return multiple weighted selections."""

    if count < 0:
        raise ValueError("count cannot be negative.")

    validate_distribution(distribution)

    random_generator = rng or random

    return random_generator.choices(
        population=list(distribution.keys()),
        weights=list(distribution.values()),
        k=count,
    )


def probability_event(
    probability: float,
    rng: random.Random | None = None,
) -> bool:
    """Return True according to the supplied probability."""

    if not 0.0 <= probability <= 1.0:
        raise ValueError(
            "probability must be between 0 and 1."
        )

    random_generator = rng or random

    return random_generator.random() < probability


# =========================================================
# BUSINESS SELECTION FUNCTIONS
# =========================================================

def choose_customer_gender(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(CUSTOMER_GENDER_WEIGHTS, rng)


def choose_customer_segment(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(CUSTOMER_SEGMENT_WEIGHTS, rng)


def choose_customer_status(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(CUSTOMER_STATUS_WEIGHTS, rng)


def choose_address_type(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(ADDRESS_TYPE_WEIGHTS, rng)


def choose_membership_billing_cycle(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(
        MEMBERSHIP_BILLING_CYCLE_WEIGHTS,
        rng,
    )


def choose_membership_status(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(
        MEMBERSHIP_STATUS_WEIGHTS,
        rng,
    )


def choose_product_status(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(PRODUCT_STATUS_WEIGHTS, rng)


def choose_supplier_status(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(SUPPLIER_STATUS_WEIGHTS, rng)


def choose_location_status(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(LOCATION_STATUS_WEIGHTS, rng)


def choose_sales_channel(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(SALES_CHANNEL_WEIGHTS, rng)


def choose_order_status(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(ORDER_STATUS_WEIGHTS, rng)


def choose_payment_method(
    sales_channel: str | None = None,
    rng: random.Random | None = None,
) -> str:
    """
    Choose a payment method compatible with the sales channel.

    CASH is restricted to store purchases, while
    CASH_ON_DELIVERY is restricted to non-store purchases.
    """

    if sales_channel is None:
        return weighted_choice(PAYMENT_METHOD_WEIGHTS, rng)

    normalized_channel = sales_channel.strip().upper()

    if normalized_channel not in SALES_CHANNELS:
        raise ValueError(
            f"Invalid sales channel: {sales_channel}"
        )

    compatible_weights = PAYMENT_METHOD_WEIGHTS.copy()

    if normalized_channel == "STORE":
        compatible_weights.pop("CASH_ON_DELIVERY")
    else:
        compatible_weights.pop("CASH")

    total = sum(compatible_weights.values())

    normalized_weights = {
        method: weight / total
        for method, weight in compatible_weights.items()
    }

    return weighted_choice(normalized_weights, rng)


def choose_payment_status(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(PAYMENT_STATUS_WEIGHTS, rng)


def choose_return_status(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(RETURN_STATUS_WEIGHTS, rng)


def choose_return_reason(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(RETURN_REASON_WEIGHTS, rng)


def choose_purchase_order_status(
    rng: random.Random | None = None,
) -> str:
    return weighted_choice(
        PURCHASE_ORDER_STATUS_WEIGHTS,
        rng,
    )


def choose_order_item_count(
    rng: random.Random | None = None,
) -> int:
    return weighted_choice(ORDER_ITEM_COUNT_WEIGHTS, rng)


def choose_item_quantity(
    rng: random.Random | None = None,
) -> int:
    return weighted_choice(ITEM_QUANTITY_WEIGHTS, rng)


def choose_discount_percentage(
    rng: random.Random | None = None,
) -> float:
    return weighted_choice(
        DISCOUNT_PERCENTAGE_WEIGHTS,
        rng,
    )


# =========================================================
# CONDITIONAL PROBABILITIES
# =========================================================

def get_return_probability(category_name: str) -> float:
    """Return category-specific return probability."""

    category_probabilities = {
        "Electronics": 0.10,
        "Fashion": 0.18,
        "Home & Kitchen": 0.08,
        "Beauty & Personal Care": 0.02,
        "Sports & Fitness": 0.09,
        "Books": 0.04,
        "Furniture": 0.07,
        "Toys & Games": 0.08,
        "Grocery": 0.01,
        "Smart Home": 0.10,
        "Mobiles & Accessories": 0.12,
        "Computers & Laptops": 0.09,
        "Appliances": 0.08,
        "Automotive": 0.07,
        "Office Supplies": 0.04,
    }

    return category_probabilities.get(
        category_name,
        0.05,
    )


def get_membership_probability(
    customer_segment: str,
) -> float:
    """Return membership probability by customer segment."""

    probabilities = {
        "STUDENT": 0.10,
        "WORKING_PROFESSIONAL": 0.24,
        "FAMILY": 0.22,
        "SENIOR_CITIZEN": 0.12,
        "SMALL_BUSINESS": 0.28,
        "PREMIUM_MEMBER": 1.00,
    }

    normalized_segment = customer_segment.strip().upper()

    if normalized_segment not in CUSTOMER_SEGMENTS:
        raise ValueError(
            f"Invalid customer segment: {customer_segment}"
        )

    return probabilities[normalized_segment]


def get_repeat_purchase_probability(
    customer_segment: str,
    is_premium_member: bool,
) -> float:
    """Return repeat-purchase probability."""

    base_probabilities = {
        "STUDENT": 0.36,
        "WORKING_PROFESSIONAL": 0.52,
        "FAMILY": 0.60,
        "SENIOR_CITIZEN": 0.43,
        "SMALL_BUSINESS": 0.66,
        "PREMIUM_MEMBER": 0.72,
    }

    normalized_segment = customer_segment.strip().upper()

    if normalized_segment not in CUSTOMER_SEGMENTS:
        raise ValueError(
            f"Invalid customer segment: {customer_segment}"
        )

    probability = base_probabilities[normalized_segment]

    if is_premium_member:
        probability += 0.10

    return min(probability, 0.90)


# =========================================================
# SEASONAL FUNCTIONS
# =========================================================

def get_demand_multiplier(
    target_date: date | datetime,
) -> float:
    """Return combined monthly, weekday and festival demand."""

    if isinstance(target_date, datetime):
        target_date = target_date.date()

    if not isinstance(target_date, date):
        raise TypeError(
            "target_date must be a date or datetime."
        )

    monthly_multiplier = MONTHLY_DEMAND_MULTIPLIERS[
        target_date.month
    ]

    weekday_multiplier = WEEKDAY_DEMAND_MULTIPLIERS[
        target_date.weekday()
    ]

    festival_season_multiplier = FESTIVAL_SEASONS.get(
        target_date.month,
        1.00,
    )

    festival_day_multiplier = (
        FESTIVAL_DEMAND_MULTIPLIERS.get(
            (target_date.month, target_date.day),
            1.00,
        )
    )

    combined_multiplier = (
        monthly_multiplier
        * weekday_multiplier
        * festival_season_multiplier
        * festival_day_multiplier
    )

    return round(combined_multiplier, 4)


# =========================================================
# MODULE VALIDATION
# =========================================================

def validate_probability_models() -> None:
    """Validate every configured probability distribution."""

    distributions = {
        "CUSTOMER_GENDER_WEIGHTS": CUSTOMER_GENDER_WEIGHTS,
        "CUSTOMER_SEGMENT_WEIGHTS": CUSTOMER_SEGMENT_WEIGHTS,
        "CUSTOMER_STATUS_WEIGHTS": CUSTOMER_STATUS_WEIGHTS,
        "ADDRESS_TYPE_WEIGHTS": ADDRESS_TYPE_WEIGHTS,
        "MEMBERSHIP_BILLING_CYCLE_WEIGHTS":
            MEMBERSHIP_BILLING_CYCLE_WEIGHTS,
        "MEMBERSHIP_STATUS_WEIGHTS":
            MEMBERSHIP_STATUS_WEIGHTS,
        "PRODUCT_STATUS_WEIGHTS": PRODUCT_STATUS_WEIGHTS,
        "SUPPLIER_STATUS_WEIGHTS": SUPPLIER_STATUS_WEIGHTS,
        "LOCATION_STATUS_WEIGHTS": LOCATION_STATUS_WEIGHTS,
        "SALES_CHANNEL_WEIGHTS": SALES_CHANNEL_WEIGHTS,
        "ORDER_STATUS_WEIGHTS": ORDER_STATUS_WEIGHTS,
        "PAYMENT_METHOD_WEIGHTS": PAYMENT_METHOD_WEIGHTS,
        "PAYMENT_STATUS_WEIGHTS": PAYMENT_STATUS_WEIGHTS,
        "RETURN_STATUS_WEIGHTS": RETURN_STATUS_WEIGHTS,
        "RETURN_REASON_WEIGHTS": RETURN_REASON_WEIGHTS,
        "PURCHASE_ORDER_STATUS_WEIGHTS":
            PURCHASE_ORDER_STATUS_WEIGHTS,
        "ORDER_ITEM_COUNT_WEIGHTS":
            ORDER_ITEM_COUNT_WEIGHTS,
        "ITEM_QUANTITY_WEIGHTS": ITEM_QUANTITY_WEIGHTS,
        "DISCOUNT_PERCENTAGE_WEIGHTS":
            DISCOUNT_PERCENTAGE_WEIGHTS,
    }

    for name, distribution in distributions.items():
        validate_distribution(distribution, name)

    constant_checks: Sequence[
        tuple[set[str], set[str], str]
    ] = (
        (
            set(CUSTOMER_GENDER_WEIGHTS),
            set(CUSTOMER_GENDERS),
            "customer gender",
        ),
        (
            set(CUSTOMER_SEGMENT_WEIGHTS),
            set(CUSTOMER_SEGMENTS),
            "customer segment",
        ),
        (
            set(SALES_CHANNEL_WEIGHTS),
            set(SALES_CHANNELS),
            "sales channel",
        ),
        (
            set(ORDER_STATUS_WEIGHTS),
            set(ORDER_STATUSES),
            "order status",
        ),
        (
            set(PAYMENT_METHOD_WEIGHTS),
            set(PAYMENT_METHODS),
            "payment method",
        ),
        (
            set(RETURN_REASON_WEIGHTS),
            set(RETURN_REASONS),
            "return reason",
        ),
    )

    for weighted_values, constant_values, name in constant_checks:
        if weighted_values != constant_values:
            raise ValueError(
                f"Probability and constant values do not "
                f"match for {name}."
            )


validate_probability_models()


if __name__ == "__main__":
    print("RetailNova probability models validated.")
    print(
        "October demand multiplier:",
        get_demand_multiplier(date(2025, 10, 20)),
    )

probability_path = (
    "/content/retailnova/python/generators/"
    "probability_models.py"
)

replace_required(
    probability_path,
    '''ORDER_STATUS_WEIGHTS = {
    "PLACED": 0.04,
    "SHIPPED": 0.06,
    "DELIVERED": 0.86,
    "CANCELLED": 0.04,
}''',
    '''ORDER_STATUS_WEIGHTS = {
    "PENDING": 0.04,
    "CONFIRMED": 0.06,
    "SHIPPED": 0.06,
    "DELIVERED": 0.80,
    "CANCELLED": 0.04,
}''',
)

replace_required(
    probability_path,
    '''RETURN_STATUS_WEIGHTS = {
    "REQUESTED": 0.12,
    "APPROVED": 0.23,
    "REJECTED": 0.10,
    "REFUNDED": 0.55,
}''',
    '''RETURN_STATUS_WEIGHTS = {
    "REQUESTED": 0.12,
    "APPROVED": 0.23,
    "REJECTED": 0.10,
    "COMPLETED": 0.55,
}''',
)

replace_required(
    probability_path,
    '''PURCHASE_ORDER_STATUS_WEIGHTS = {
    "PENDING": 0.12,
    "RECEIVED": 0.84,
    "CANCELLED": 0.04,
}''',
    '''PURCHASE_ORDER_STATUS_WEIGHTS = {
    "CREATED": 0.08,
    "APPROVED": 0.08,
    "RECEIVED": 0.80,
    "CANCELLED": 0.04,
}''',
)
