

"""
RetailNova Decision Intelligence Platform
Return Data Generator

Generates returned-order-item records from eligible,
delivered RetailNova orders.

Author: Hardik Narigra
"""

from datetime import timedelta
from decimal import Decimal
from pathlib import Path

import pandas as pd

try:
    from business_rules import (
        CATEGORY_RETURN_ELIGIBILITY,
        round_currency,
    )
    from config import CONFIG, GeneratorConfig
    from constants import (
        CSV_FILE_NAMES,
        RETURN_REASONS,
        RETURN_STATUSES,
    )
    from probability_models import (
        RETURN_REASON_WEIGHTS,
    )
    from utils import (
        dataframe_summary,
        export_dataframe,
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
        "before importing return_generator."
    ) from error


RETURN_COLUMNS = [
    "return_id",
    "order_item_id",
    "return_date",
    "quantity",
    "reason",
    "return_status",
    "refund_amount",
    "created_at",
    "updated_at",
]


def load_return_dependencies(
    config: GeneratorConfig = CONFIG,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """Load order, item, product, category and payment data."""

    paths = {
        "orders": (
            config.output_directory
            / CSV_FILE_NAMES["orders"]
        ),
        "order_item": (
            config.output_directory
            / CSV_FILE_NAMES["order_item"]
        ),
        "product": (
            config.output_directory
            / CSV_FILE_NAMES["product"]
        ),
        "category": (
            config.output_directory
            / CSV_FILE_NAMES["category"]
        ),
        "payment": (
            config.output_directory
            / CSV_FILE_NAMES["payment"]
        ),
    }

    missing_files = [
        str(path)
        for path in paths.values()
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Return dependencies are missing: {missing_files}"
        )

    orders = pd.read_csv(paths["orders"])
    order_items = pd.read_csv(paths["order_item"])
    products = pd.read_csv(paths["product"])
    categories = pd.read_csv(paths["category"])
    payments = pd.read_csv(paths["payment"])

    validate_required_columns(
        orders,
        [
            "order_id",
            "order_date",
            "order_status",
        ],
        "orders",
    )

    validate_required_columns(
        order_items,
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "line_total",
        ],
        "order_item",
    )

    validate_required_columns(
        products,
        [
            "product_id",
            "category_id",
        ],
        "product",
    )

    validate_required_columns(
        categories,
        [
            "category_id",
            "category_name",
        ],
        "category",
    )

    validate_required_columns(
        payments,
        [
            "order_id",
            "payment_status",
        ],
        "payment",
    )

    return (
        orders,
        order_items,
        products,
        categories,
        payments,
    )


def build_eligible_return_items(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    categories: pd.DataFrame,
    payments: pd.DataFrame,
) -> pd.DataFrame:
    """Create the pool of eligible delivered order items."""

    eligible_categories = {
        category_name
        for category_name, eligible
        in CATEGORY_RETURN_ELIGIBILITY.items()
        if eligible
    }

    eligible_items = (
        order_items
        .merge(
            orders[
                [
                    "order_id",
                    "order_date",
                    "order_status",
                ]
            ],
            on="order_id",
            how="inner",
            validate="many_to_one",
        )
        .merge(
            products[
                [
                    "product_id",
                    "category_id",
                ]
            ],
            on="product_id",
            how="inner",
            validate="many_to_one",
        )
        .merge(
            categories[
                [
                    "category_id",
                    "category_name",
                ]
            ],
            on="category_id",
            how="inner",
            validate="many_to_one",
        )
        .merge(
            payments[
                [
                    "order_id",
                    "payment_status",
                ]
            ],
            on="order_id",
            how="inner",
            validate="many_to_one",
        )
    )

    eligible_items = eligible_items.loc[
        eligible_items["order_status"].eq(
            "DELIVERED"
        )
        & eligible_items["category_name"].isin(
            eligible_categories
        )
        & eligible_items["payment_status"].isin(
            ["SUCCESS", "REFUNDED"]
        )
    ].copy()

    if eligible_items.empty:
        raise ValueError(
            "No delivered, return-eligible order items found."
        )

    return eligible_items


def select_return_items(
    eligible_items: pd.DataFrame,
    return_count: int,
    rng,
) -> pd.DataFrame:
    """Select unique return items and retain refunded cases."""

    if return_count > len(eligible_items):
        raise ValueError(
            f"Requested {return_count} returns but only "
            f"{len(eligible_items)} items are eligible."
        )

    refunded_candidates = (
        eligible_items.loc[
            eligible_items[
                "payment_status"
            ].eq("REFUNDED")
        ]
        .drop_duplicates("order_id")
    )

    selected_indices = set(
        refunded_candidates.index.tolist()[
            :return_count
        ]
    )

    remaining_indices = [
        index
        for index in eligible_items.index
        if index not in selected_indices
    ]

    rng.shuffle(remaining_indices)

    required_remaining = (
        return_count - len(selected_indices)
    )

    selected_indices.update(
        remaining_indices[:required_remaining]
    )

    selected_items = eligible_items.loc[
        list(selected_indices)
    ].copy()

    selected_items = selected_items.sample(
        frac=1,
        random_state=42,
    ).reset_index(drop=True)

    return selected_items


def choose_return_status(
    payment_status: str,
    rng,
) -> str:
    """Choose a status consistent with payment state."""

    if payment_status == "REFUNDED":
        return "REFUNDED"

    status_model = {
        "REQUESTED": 0.30,
        "APPROVED": 0.45,
        "REJECTED": 0.25,
    }

    return rng.choices(
        list(status_model.keys()),
        weights=list(status_model.values()),
        k=1,
    )[0]


def generate_returns(
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    categories: pd.DataFrame,
    payments: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Generate return records."""

    return_count = config.get_record_count("returns")

    rng = set_random_seeds(config.random_seed + 6)

    eligible_items = build_eligible_return_items(
        orders,
        order_items,
        products,
        categories,
        payments,
    )

    selected_items = select_return_items(
        eligible_items,
        return_count,
        rng,
    )

    reason_values = list(
        RETURN_REASON_WEIGHTS.keys()
    )

    reason_weights = list(
        RETURN_REASON_WEIGHTS.values()
    )

    records = []

    for return_id, item in enumerate(
        selected_items.itertuples(),
        start=1,
    ):
        ordered_quantity = int(item.quantity)

        returned_quantity = rng.randint(
            1,
            ordered_quantity,
        )

        return_status = choose_return_status(
            item.payment_status,
            rng,
        )

        reason = rng.choices(
            reason_values,
            weights=reason_weights,
            k=1,
        )[0]

        order_datetime = pd.Timestamp(
            item.order_date
        )

        maximum_return_datetime = min(
            order_datetime + timedelta(days=15),
            pd.Timestamp(
                config.simulation_end_date
            )
            + timedelta(
                hours=23,
                minutes=59,
            ),
        )

        available_minutes = max(
            0,
            int(
                (
                    maximum_return_datetime
                    - order_datetime
                ).total_seconds()
                // 60
            ),
        )

        return_datetime = (
            order_datetime
            + timedelta(
                minutes=rng.randint(
                    0,
                    available_minutes,
                )
            )
        )

        return_timestamp = (
            return_datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + "+00:00"
        )

        if return_status in [
            "APPROVED",
            "REFUNDED",
        ]:
            refund_amount = round_currency(
                Decimal(str(item.line_total))
                * Decimal(returned_quantity)
                / Decimal(ordered_quantity)
            )

        else:
            refund_amount = Decimal("0.00")

        records.append(
            {
                "return_id": return_id,
                "order_item_id": int(
                    item.order_item_id
                ),
                "return_date": return_timestamp,
                "quantity": returned_quantity,
                "reason": reason,
                "return_status": return_status,
                "refund_amount": refund_amount,
                "created_at": return_timestamp,
                "updated_at": return_timestamp,
            }
        )

    return_dataframe = pd.DataFrame(
        records,
        columns=RETURN_COLUMNS,
    )

    validate_returns(
        return_dataframe,
        orders,
        order_items,
        products,
        categories,
        payments,
        config,
    )

    return return_dataframe


def validate_returns(
    dataframe: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    categories: pd.DataFrame,
    payments: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate return records before export."""

    expected_count = config.get_record_count("returns")

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} returns, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != RETURN_COLUMNS:
        raise ValueError(
            "Return columns do not match the "
            "PostgreSQL return table."
        )

    validate_primary_key(
        dataframe,
        "return_id",
        "return",
    )

    validate_not_null_columns(
        dataframe,
        RETURN_COLUMNS,
        "return",
    )

    validate_foreign_key(
        dataframe,
        "order_item_id",
        order_items,
        "order_item_id",
        "return.order_item_id -> "
        "order_item.order_item_id",
    )

    validate_allowed_values(
        dataframe,
        "reason",
        RETURN_REASONS,
        "return",
    )

    validate_allowed_values(
        dataframe,
        "return_status",
        RETURN_STATUSES,
        "return",
    )

    validate_non_negative(
        dataframe,
        ["refund_amount"],
        "return",
    )

    if dataframe[
        "order_item_id"
    ].duplicated().any():
        raise ValueError(
            "An order item cannot be returned twice "
            "in the current model."
        )

    item_lookup = (
        order_items.set_index("order_item_id")
    )

    ordered_quantities = dataframe[
        "order_item_id"
    ].map(item_lookup["quantity"])

    if (
        (dataframe["quantity"] <= 0)
        | (
            dataframe["quantity"]
            > ordered_quantities
        )
    ).any():
        raise ValueError(
            "Returned quantity must be between one "
            "and the purchased quantity."
        )

    maximum_refunds = dataframe[
        "order_item_id"
    ].map(item_lookup["line_total"])

    if (
        dataframe["refund_amount"].astype(float)
        > maximum_refunds.astype(float) + 0.001
    ).any():
        raise ValueError(
            "Refund amount exceeds original line total."
        )

    zero_refund_statuses = dataframe[
        "return_status"
    ].isin(["REQUESTED", "REJECTED"])

    if (
        dataframe.loc[
            zero_refund_statuses,
            "refund_amount",
        ].astype(float) != 0
    ).any():
        raise ValueError(
            "Requested and rejected returns must "
            "have zero refund amount."
        )


def export_returns(
    dataframe: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
    categories: pd.DataFrame,
    payments: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export return.csv."""

    validate_returns(
        dataframe,
        orders,
        order_items,
        products,
        categories,
        payments,
        config,
    )

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["return"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=RETURN_COLUMNS,
    )


def generate_and_export_returns(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Generate and export returns."""

    (
        orders,
        order_items,
        products,
        categories,
        payments,
    ) = load_return_dependencies(config)

    return_dataframe = generate_returns(
        orders,
        order_items,
        products,
        categories,
        payments,
        config,
    )

    output_path = export_returns(
        return_dataframe,
        orders,
        order_items,
        products,
        categories,
        payments,
        config,
    )

    return return_dataframe, output_path


if __name__ == "__main__":
    return_df, csv_path = (
        generate_and_export_returns()
    )

    print("Return generation completed.")
    print(dataframe_summary(return_df, "return"))
    print(f"CSV: {csv_path}")
