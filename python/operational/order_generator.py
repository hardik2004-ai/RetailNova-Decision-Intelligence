

"""
RetailNova Decision Intelligence Platform
Order and Order-Item Data Generator

Generates orders.csv and order_item.csv as one internally
consistent transactional dataset.

Author: Hardik Narigra
"""

from decimal import Decimal
from pathlib import Path

import pandas as pd

try:
    from business_rules import (
        calculate_discount_amount,
        round_currency,
    )
    from config import CONFIG, GeneratorConfig
    from constants import (
        CSV_FILE_NAMES,
        ORDER_STATUSES,
        SALES_CHANNELS,
    )
    from probability_models import (
        DISCOUNT_PERCENTAGE_WEIGHTS,
        ITEM_QUANTITY_WEIGHTS,
        ORDER_ITEM_COUNT_WEIGHTS,
        ORDER_STATUS_WEIGHTS,
        SALES_CHANNEL_WEIGHTS,
    )
    from utils import (
        dataframe_summary,
        date_to_business_datetime,
        export_dataframe,
        random_date_between,
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
        "before importing order_generator."
    ) from error


ORDER_COLUMNS = [
    "order_id",
    "customer_id",
    "location_id",
    "order_date",
    "sales_channel",
    "order_status",
    "total_amount",
    "created_at",
    "updated_at",
]


ORDER_ITEM_COLUMNS = [
    "order_item_id",
    "order_id",
    "product_id",
    "quantity",
    "unit_price",
    "discount_amount",
    "line_total",
    "created_at",
    "updated_at",
]


def weighted_choice(
    values_and_weights: dict,
    rng,
):
    """Choose one value from a weighted mapping."""

    return rng.choices(
        list(values_and_weights.keys()),
        weights=list(values_and_weights.values()),
        k=1,
    )[0]


def load_order_dependencies(
    config: GeneratorConfig = CONFIG,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    """Load customer, location and product datasets."""

    customer_path = (
        config.output_directory
        / CSV_FILE_NAMES["customer"]
    )

    location_path = (
        config.output_directory
        / CSV_FILE_NAMES["location"]
    )

    product_path = (
        config.output_directory
        / CSV_FILE_NAMES["product"]
    )

    required_paths = [
        customer_path,
        location_path,
        product_path,
    ]

    missing_files = [
        str(path)
        for path in required_paths
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            f"Order dependencies are missing: {missing_files}"
        )

    customer_dataframe = pd.read_csv(
        customer_path,
        parse_dates=["registration_date"],
    )

    location_dataframe = pd.read_csv(
        location_path
    )

    product_dataframe = pd.read_csv(
        product_path
    )

    validate_required_columns(
        customer_dataframe,
        [
            "customer_id",
            "registration_date",
        ],
        "customer",
    )

    validate_required_columns(
        location_dataframe,
        [
            "location_id",
            "location_type",
        ],
        "location",
    )

    validate_required_columns(
        product_dataframe,
        [
            "product_id",
            "unit_price",
        ],
        "product",
    )

    return (
        customer_dataframe,
        location_dataframe,
        product_dataframe,
    )


def generate_item_counts(
    order_count: int,
    required_item_count: int,
    rng,
) -> list[int]:
    """Create weighted counts totalling the exact requirement."""

    counts = [
        weighted_choice(
            ORDER_ITEM_COUNT_WEIGHTS,
            rng,
        )
        for _ in range(order_count)
    ]

    while sum(counts) < required_item_count:
        eligible_indices = [
            index
            for index, count in enumerate(counts)
            if count < max(ORDER_ITEM_COUNT_WEIGHTS)
        ]

        selected_index = rng.choice(
            eligible_indices
        )

        counts[selected_index] += 1

    while sum(counts) > required_item_count:
        eligible_indices = [
            index
            for index, count in enumerate(counts)
            if count > min(ORDER_ITEM_COUNT_WEIGHTS)
        ]

        selected_index = rng.choice(
            eligible_indices
        )

        counts[selected_index] -= 1

    if sum(counts) != required_item_count:
        raise RuntimeError(
            "Unable to reconcile order-item counts."
        )

    return counts


def choose_fulfilment_location(
    sales_channel: str,
    store_location_ids: list[int],
    warehouse_location_ids: list[int],
    rng,
) -> int:
    """Choose a realistic fulfilment location."""

    if sales_channel == "STORE":
        return rng.choice(store_location_ids)

    if (
        warehouse_location_ids
        and rng.random() < 0.75
    ):
        return rng.choice(warehouse_location_ids)

    return rng.choice(store_location_ids)


def generate_orders_and_items(
    customer_dataframe: pd.DataFrame,
    location_dataframe: pd.DataFrame,
    product_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Generate linked orders and order items."""

    order_count = config.get_record_count("orders")

    required_item_count = config.get_record_count(
        "order_items"
    )

    rng = set_random_seeds(config.random_seed + 4)

    customer_records = [
        (
            int(row.customer_id),
            pd.Timestamp(
                row.registration_date
            ).date(),
        )
        for row in customer_dataframe.itertuples()
    ]

    store_location_ids = (
        location_dataframe.loc[
            location_dataframe[
                "location_type"
            ].eq("STORE"),
            "location_id",
        ]
        .astype(int)
        .tolist()
    )

    warehouse_location_ids = (
        location_dataframe.loc[
            location_dataframe[
                "location_type"
            ].eq("WAREHOUSE"),
            "location_id",
        ]
        .astype(int)
        .tolist()
    )

    product_price_lookup = {
        int(row.product_id): Decimal(
            str(row.unit_price)
        )
        for row in product_dataframe.itertuples()
    }

    product_ids = list(
        product_price_lookup.keys()
    )

    item_counts = generate_item_counts(
        order_count,
        required_item_count,
        rng,
    )

    order_records = []
    order_item_records = []

    order_item_id = 1

    for order_id in range(1, order_count + 1):
        customer_id, registration_date = rng.choice(
            customer_records
        )

        order_calendar_date = random_date_between(
            registration_date,
            config.simulation_end_date,
            rng,
        )

        order_datetime = date_to_business_datetime(
            order_calendar_date,
            rng,
        )

        order_timestamp = (
            order_datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            + "+00:00"
        )

        sales_channel = weighted_choice(
            SALES_CHANNEL_WEIGHTS,
            rng,
        )

        order_status = weighted_choice(
            ORDER_STATUS_WEIGHTS,
            rng,
        )

        location_id = choose_fulfilment_location(
            sales_channel,
            store_location_ids,
            warehouse_location_ids,
            rng,
        )

        item_count = item_counts[order_id - 1]

        selected_product_ids = rng.sample(
            product_ids,
            item_count,
        )

        order_total = Decimal("0.00")

        for product_id in selected_product_ids:
            quantity = weighted_choice(
                ITEM_QUANTITY_WEIGHTS,
                rng,
            )

            discount_percentage = weighted_choice(
                DISCOUNT_PERCENTAGE_WEIGHTS,
                rng,
            )

            unit_price = product_price_lookup[
                product_id
            ]

            gross_amount = round_currency(
                unit_price * quantity
            )

            discount_amount = (
                calculate_discount_amount(
                    gross_amount,
                    discount_percentage,
                )
            )

            line_total = round_currency(
                gross_amount - discount_amount
            )

            order_total = round_currency(
                order_total + line_total
            )

            order_item_records.append(
                {
                    "order_item_id": order_item_id,
                    "order_id": order_id,
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount_amount": discount_amount,
                    "line_total": line_total,
                    "created_at": order_timestamp,
                    "updated_at": order_timestamp,
                }
            )

            order_item_id += 1

        order_records.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "location_id": location_id,
                "order_date": order_timestamp,
                "sales_channel": sales_channel,
                "order_status": order_status,
                "total_amount": order_total,
                "created_at": order_timestamp,
                "updated_at": order_timestamp,
            }
        )

    order_dataframe = pd.DataFrame(
        order_records,
        columns=ORDER_COLUMNS,
    )

    order_item_dataframe = pd.DataFrame(
        order_item_records,
        columns=ORDER_ITEM_COLUMNS,
    )

    validate_orders_and_items(
        order_dataframe,
        order_item_dataframe,
        customer_dataframe,
        location_dataframe,
        product_dataframe,
        config,
    )

    return order_dataframe, order_item_dataframe


def validate_orders_and_items(
    order_dataframe: pd.DataFrame,
    order_item_dataframe: pd.DataFrame,
    customer_dataframe: pd.DataFrame,
    location_dataframe: pd.DataFrame,
    product_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate transactional consistency."""

    if len(order_dataframe) != config.get_record_count(
        "orders"
    ):
        raise ValueError(
            "Unexpected number of order records."
        )

    if len(
        order_item_dataframe
    ) != config.get_record_count("order_items"):
        raise ValueError(
            "Unexpected number of order-item records."
        )

    if list(order_dataframe.columns) != ORDER_COLUMNS:
        raise ValueError(
            "Order columns do not match the database."
        )

    if (
        list(order_item_dataframe.columns)
        != ORDER_ITEM_COLUMNS
    ):
        raise ValueError(
            "Order-item columns do not match the database."
        )

    validate_primary_key(
        order_dataframe,
        "order_id",
        "orders",
    )

    validate_primary_key(
        order_item_dataframe,
        "order_item_id",
        "order_item",
    )

    validate_not_null_columns(
        order_dataframe,
        ORDER_COLUMNS,
        "orders",
    )

    validate_not_null_columns(
        order_item_dataframe,
        ORDER_ITEM_COLUMNS,
        "order_item",
    )

    validate_foreign_key(
        order_dataframe,
        "customer_id",
        customer_dataframe,
        "customer_id",
        "orders.customer_id -> customer.customer_id",
    )

    validate_foreign_key(
        order_dataframe,
        "location_id",
        location_dataframe,
        "location_id",
        "orders.location_id -> location.location_id",
    )

    validate_foreign_key(
        order_item_dataframe,
        "order_id",
        order_dataframe,
        "order_id",
        "order_item.order_id -> orders.order_id",
    )

    validate_foreign_key(
        order_item_dataframe,
        "product_id",
        product_dataframe,
        "product_id",
        "order_item.product_id -> product.product_id",
    )

    validate_allowed_values(
        order_dataframe,
        "sales_channel",
        SALES_CHANNELS,
        "orders",
    )

    validate_allowed_values(
        order_dataframe,
        "order_status",
        ORDER_STATUSES,
        "orders",
    )

    validate_non_negative(
        order_dataframe,
        ["total_amount"],
        "orders",
    )

    validate_non_negative(
        order_item_dataframe,
        [
            "unit_price",
            "discount_amount",
            "line_total",
        ],
        "order_item",
    )

    if (
        order_item_dataframe["quantity"] <= 0
    ).any():
        raise ValueError(
            "Order-item quantity must be positive."
        )

    duplicate_products = (
        order_item_dataframe.duplicated(
            subset=[
                "order_id",
                "product_id",
            ]
        )
    )

    if duplicate_products.any():
        raise ValueError(
            "An order cannot contain the same product twice."
        )

    item_counts = (
        order_item_dataframe.groupby("order_id")
        .size()
    )

    if not item_counts.between(1, 8).all():
        raise ValueError(
            "Orders must contain between 1 and 8 items."
        )

    calculated_totals = (
        order_item_dataframe.groupby("order_id")[
            "line_total"
        ]
        .apply(
            lambda values: sum(
                Decimal(str(value))
                for value in values
            )
        )
        .map(round_currency)
    )

    stored_totals = (
        order_dataframe.set_index("order_id")[
            "total_amount"
        ]
        .map(
            lambda value: round_currency(
                Decimal(str(value))
            )
        )
    )

    mismatched_totals = (
        calculated_totals != stored_totals
    )

    if mismatched_totals.any():
        raise ValueError(
            "Order totals do not reconcile with "
            "order-item totals."
        )

    customer_registration = (
        customer_dataframe.set_index("customer_id")[
            "registration_date"
        ]
    )

    order_dates = pd.to_datetime(
        order_dataframe["order_date"],
        utc=True,
    ).dt.tz_localize(None)

    registration_dates = pd.to_datetime(
        order_dataframe["customer_id"].map(
            customer_registration
        )
    )

    if (order_dates < registration_dates).any():
        raise ValueError(
            "Orders cannot precede customer registration."
        )


def export_orders_and_items(
    order_dataframe: pd.DataFrame,
    order_item_dataframe: pd.DataFrame,
    customer_dataframe: pd.DataFrame,
    location_dataframe: pd.DataFrame,
    product_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> tuple[Path, Path]:
    """Validate and export both transaction files."""

    validate_orders_and_items(
        order_dataframe,
        order_item_dataframe,
        customer_dataframe,
        location_dataframe,
        product_dataframe,
        config,
    )

    order_path = (
        config.output_directory
        / CSV_FILE_NAMES["orders"]
    )

    order_item_path = (
        config.output_directory
        / CSV_FILE_NAMES["order_item"]
    )

    export_dataframe(
        order_dataframe,
        order_path,
        expected_columns=ORDER_COLUMNS,
    )

    export_dataframe(
        order_item_dataframe,
        order_item_path,
        expected_columns=ORDER_ITEM_COLUMNS,
    )

    return order_path, order_item_path


def generate_and_export_orders(
    config: GeneratorConfig = CONFIG,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    Path,
    Path,
]:
    """Generate and export orders and items."""

    (
        customer_dataframe,
        location_dataframe,
        product_dataframe,
    ) = load_order_dependencies(config)

    (
        order_dataframe,
        order_item_dataframe,
    ) = generate_orders_and_items(
        customer_dataframe,
        location_dataframe,
        product_dataframe,
        config,
    )

    order_path, order_item_path = (
        export_orders_and_items(
            order_dataframe,
            order_item_dataframe,
            customer_dataframe,
            location_dataframe,
            product_dataframe,
            config,
        )
    )

    return (
        order_dataframe,
        order_item_dataframe,
        order_path,
        order_item_path,
    )


if __name__ == "__main__":
    (
        orders_df,
        order_items_df,
        orders_csv,
        order_items_csv,
    ) = generate_and_export_orders()

    print(dataframe_summary(orders_df, "orders"))
    print(
        dataframe_summary(
            order_items_df,
            "order_item",
        )
    )
    print(f"Orders CSV: {orders_csv}")
    print(f"Order items CSV: {order_items_csv}")
