
"""
RetailNova Decision Intelligence Platform
Payment Data Generator

Generates one payment record for every RetailNova order.

Author: Hardik Narigra
"""

from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pandas as pd

try:
    from config import CONFIG, GeneratorConfig
    from constants import (
        CSV_FILE_NAMES,
        PAYMENT_METHODS,
        PAYMENT_STATUSES,
    )
    from probability_models import (
        PAYMENT_METHOD_WEIGHTS,
    )
    from utils import (
        dataframe_summary,
        export_dataframe,
        generate_sequential_code,
        set_random_seeds,
        validate_allowed_values,
        validate_foreign_key,
        validate_non_negative,
        validate_not_null_columns,
        validate_primary_key,
        validate_required_columns,
    )
except ImportError as error:
    raise ImportError(
        "Unable to import RetailNova generator modules. "
        "Add /content/retailnova/python/generators to sys.path "
        "before importing payment_generator."
    ) from error


PAYMENT_COLUMNS = [
    "payment_id",
    "order_id",
    "payment_method",
    "payment_status",
    "payment_date",
    "amount",
    "transaction_reference",
    "created_at",
    "updated_at",
]


def load_order_data(
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Load orders.csv for payment generation."""

    order_path = (
        config.output_directory
        / CSV_FILE_NAMES["orders"]
    )

    if not order_path.exists():
        raise FileNotFoundError(
            f"Order dataset not found: {order_path}"
        )

    order_dataframe = pd.read_csv(
        order_path
    )

    validate_required_columns(
        order_dataframe,
        [
            "order_id",
            "order_date",
            "sales_channel",
            "order_status",
            "total_amount",
        ],
        "orders",
    )

    return order_dataframe


def choose_payment_method(
    sales_channel: str,
    rng,
) -> str:
    """Choose a payment method appropriate to the channel."""

    if sales_channel == "STORE":
        allowed_methods = [
            "UPI",
            "CREDIT_CARD",
            "DEBIT_CARD",
            "NET_BANKING",
            "WALLET",
            "CASH",
        ]

    else:
        allowed_methods = [
            "UPI",
            "CREDIT_CARD",
            "DEBIT_CARD",
            "NET_BANKING",
            "WALLET",
            "CASH_ON_DELIVERY",
        ]

    weights = [
        PAYMENT_METHOD_WEIGHTS[method]
        for method in allowed_methods
    ]

    return rng.choices(
        allowed_methods,
        weights=weights,
        k=1,
    )[0]


def choose_payment_status(
    order_status: str,
    rng,
) -> str:
    """Choose a status consistent with order state."""

    status_models = {
        "DELIVERED": {
            "SUCCESS": 0.97,
            "REFUNDED": 0.03,
        },
        "SHIPPED": {
            "SUCCESS": 0.97,
            "PENDING": 0.03,
        },
        "PLACED": {
            "SUCCESS": 0.80,
            "PENDING": 0.15,
            "FAILED": 0.05,
        },
        "CANCELLED": {
            "FAILED": 0.70,
            "REFUNDED": 0.30,
        },
    }

    if order_status not in status_models:
        raise ValueError(
            f"Unsupported order status: {order_status}"
        )

    model = status_models[order_status]

    return rng.choices(
        list(model.keys()),
        weights=list(model.values()),
        k=1,
    )[0]


def generate_payments(
    order_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Generate one payment per order."""

    expected_count = config.get_record_count(
        "payments"
    )

    if expected_count != len(order_dataframe):
        raise ValueError(
            "Payment count must equal order count. "
            f"Configured={expected_count}, "
            f"orders={len(order_dataframe)}."
        )

    rng = set_random_seeds(config.random_seed + 5)

    records = []

    for payment_id, order in enumerate(
        order_dataframe.itertuples(),
        start=1,
    ):
        order_id = int(order.order_id)
        order_status = order.order_status
        sales_channel = order.sales_channel

        payment_method = choose_payment_method(
            sales_channel,
            rng,
        )

        payment_status = choose_payment_status(
            order_status,
            rng,
        )

        order_datetime = pd.Timestamp(
            order.order_date
        )

        if payment_status == "PENDING":
            payment_date = None
            transaction_reference = None

        else:
            payment_delay_minutes = rng.randint(
                1,
                120,
            )

            payment_datetime = (
                order_datetime
                + timedelta(
                    minutes=payment_delay_minutes
                )
            )

            payment_date = (
                payment_datetime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                + "+00:00"
            )

            transaction_reference = (
                generate_sequential_code(
                    "TXN",
                    payment_id,
                    width=12,
                )
            )

        created_at = (
            order_datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + "+00:00"
        )

        records.append(
            {
                "payment_id": payment_id,
                "order_id": order_id,
                "payment_method": payment_method,
                "payment_status": payment_status,
                "payment_date": payment_date,
                "amount": Decimal(
                    str(order.total_amount)
                ),
                "transaction_reference": (
                    transaction_reference
                ),
                "created_at": created_at,
                "updated_at": (
                    payment_date or created_at
                ),
            }
        )

    payment_dataframe = pd.DataFrame(
        records,
        columns=PAYMENT_COLUMNS,
    )

    validate_payments(
        payment_dataframe,
        order_dataframe,
        config,
    )

    return payment_dataframe


def validate_payments(
    dataframe: pd.DataFrame,
    order_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate payments before export."""

    expected_count = config.get_record_count(
        "payments"
    )

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} payments, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != PAYMENT_COLUMNS:
        raise ValueError(
            "Payment columns do not match the "
            "PostgreSQL payment table."
        )

    validate_primary_key(
        dataframe,
        "payment_id",
        "payment",
    )

    validate_not_null_columns(
        dataframe,
        [
            "payment_id",
            "order_id",
            "payment_method",
            "payment_status",
            "amount",
            "created_at",
            "updated_at",
        ],
        "payment",
    )

    validate_foreign_key(
        dataframe,
        "order_id",
        order_dataframe,
        "order_id",
        "payment.order_id -> orders.order_id",
    )

    validate_allowed_values(
        dataframe,
        "payment_method",
        PAYMENT_METHODS,
        "payment",
    )

    validate_allowed_values(
        dataframe,
        "payment_status",
        PAYMENT_STATUSES,
        "payment",
    )

    validate_non_negative(
        dataframe,
        ["amount"],
        "payment",
    )

    if dataframe["order_id"].duplicated().any():
        raise ValueError(
            "Each order must have exactly one payment."
        )

    non_null_references = dataframe[
        "transaction_reference"
    ].dropna()

    if non_null_references.duplicated().any():
        raise ValueError(
            "transaction_reference must be unique."
        )

    pending_rows = dataframe[
        "payment_status"
    ].eq("PENDING")

    if dataframe.loc[
        pending_rows,
        "payment_date",
    ].notna().any():
        raise ValueError(
            "Pending payments must have a null payment_date."
        )

    if dataframe.loc[
        pending_rows,
        "transaction_reference",
    ].notna().any():
        raise ValueError(
            "Pending payments must have a null "
            "transaction_reference."
        )

    completed_rows = ~pending_rows

    if dataframe.loc[
        completed_rows,
        "payment_date",
    ].isna().any():
        raise ValueError(
            "Non-pending payments require a payment_date."
        )

    if dataframe.loc[
        completed_rows,
        "transaction_reference",
    ].isna().any():
        raise ValueError(
            "Non-pending payments require a "
            "transaction_reference."
        )

    order_amounts = (
        order_dataframe.set_index("order_id")[
            "total_amount"
        ]
        .map(lambda value: Decimal(str(value)))
    )

    payment_amounts = (
        dataframe.set_index("order_id")["amount"]
        .map(lambda value: Decimal(str(value)))
    )

    if not payment_amounts.eq(
        order_amounts
    ).all():
        raise ValueError(
            "Payment amounts must equal order totals."
        )

    payment_dates = pd.to_datetime(
        dataframe["payment_date"],
        utc=True,
    )

    order_date_lookup = (
        order_dataframe.set_index("order_id")[
            "order_date"
        ]
    )

    corresponding_order_dates = pd.to_datetime(
        dataframe["order_id"].map(
            order_date_lookup
        ),
        utc=True,
    )

    invalid_date_order = (
        payment_dates.notna()
        & (
            payment_dates
            < corresponding_order_dates
        )
    )

    if invalid_date_order.any():
        raise ValueError(
            "payment_date cannot precede order_date."
        )


def export_payments(
    dataframe: pd.DataFrame,
    order_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export payment.csv."""

    validate_payments(
        dataframe,
        order_dataframe,
        config,
    )

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["payment"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=PAYMENT_COLUMNS,
    )


def generate_and_export_payments(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Generate and export payment data."""

    order_dataframe = load_order_data(config)

    payment_dataframe = generate_payments(
        order_dataframe,
        config,
    )

    output_path = export_payments(
        payment_dataframe,
        order_dataframe,
        config,
    )

    return payment_dataframe, output_path


if __name__ == "__main__":
    payment_df, csv_path = (
        generate_and_export_payments()
    )

    print("Payment generation completed.")
    print(
        dataframe_summary(
            payment_df,
            "payment",
        )
    )
    print(f"CSV: {csv_path}")
