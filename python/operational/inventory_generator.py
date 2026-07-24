
"""
RetailNova Decision Intelligence Platform
Inventory Data Generator

Generates current product inventory across RetailNova
stores and warehouses.

Author: Hardik Narigra
"""

from datetime import timedelta
from pathlib import Path

import pandas as pd

try:
    from config import CONFIG, GeneratorConfig
    from constants import CSV_FILE_NAMES
    from utils import (
        dataframe_summary,
        export_dataframe,
        random_date_between,
        set_random_seeds,
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
        "before importing inventory_generator."
    ) from error


INVENTORY_COLUMNS = [
    "inventory_id",
    "product_id",
    "location_id",
    "quantity_on_hand",
    "reorder_level",
    "last_stock_update",
    "created_at",
    "updated_at",
]


def load_inventory_dependencies(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load product and location datasets."""

    product_path = (
        config.output_directory
        / CSV_FILE_NAMES["product"]
    )

    location_path = (
        config.output_directory
        / CSV_FILE_NAMES["location"]
    )

    missing_files = [
        str(path)
        for path in [product_path, location_path]
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Inventory dependencies are missing: "
            f"{missing_files}"
        )

    product_dataframe = pd.read_csv(product_path)
    location_dataframe = pd.read_csv(location_path)

    validate_required_columns(
        product_dataframe,
        ["product_id"],
        "product",
    )

    validate_required_columns(
        location_dataframe,
        [
            "location_id",
            "location_type",
        ],
        "location",
    )

    return product_dataframe, location_dataframe


def select_inventory_pairs(
    product_ids: list[int],
    location_ids: list[int],
    required_count: int,
    rng,
) -> list[tuple[int, int]]:
    """Select unique pairs while covering every parent ID."""

    all_pairs = [
        (product_id, location_id)
        for product_id in product_ids
        for location_id in location_ids
    ]

    if required_count > len(all_pairs):
        raise ValueError(
            f"Cannot generate {required_count} unique inventory "
            f"records from only {len(all_pairs)} combinations."
        )

    selected_pairs: set[tuple[int, int]] = set()

    # Guarantee that every product appears.
    for product_id in product_ids:
        selected_pairs.add(
            (
                product_id,
                rng.choice(location_ids),
            )
        )

    # Guarantee that every location appears.
    for location_id in location_ids:
        selected_pairs.add(
            (
                rng.choice(product_ids),
                location_id,
            )
        )

    remaining_pairs = [
        pair
        for pair in all_pairs
        if pair not in selected_pairs
    ]

    rng.shuffle(remaining_pairs)

    required_remaining = (
        required_count - len(selected_pairs)
    )

    selected_pairs.update(
        remaining_pairs[:required_remaining]
    )

    final_pairs = list(selected_pairs)
    rng.shuffle(final_pairs)

    if len(final_pairs) != required_count:
        raise RuntimeError(
            "Unable to generate the required number "
            "of inventory combinations."
        )

    return final_pairs


def generate_stock_values(
    location_type: str,
    rng,
) -> tuple[int, int]:
    """Generate quantity and reorder level."""

    if location_type == "WAREHOUSE":
        reorder_level = rng.randint(40, 100)
    else:
        reorder_level = rng.randint(5, 30)

    stock_scenario = rng.choices(
        [
            "OUT_OF_STOCK",
            "LOW_STOCK",
            "HEALTHY",
            "OVERSTOCK",
        ],
        weights=[
            0.06,
            0.16,
            0.63,
            0.15,
        ],
        k=1,
    )[0]

    if stock_scenario == "OUT_OF_STOCK":
        quantity_on_hand = 0

    elif stock_scenario == "LOW_STOCK":
        quantity_on_hand = rng.randint(
            1,
            max(1, reorder_level - 1),
        )

    elif stock_scenario == "HEALTHY":
        quantity_on_hand = rng.randint(
            reorder_level,
            reorder_level * 3,
        )

    else:
        quantity_on_hand = rng.randint(
            reorder_level * 3 + 1,
            reorder_level * 6,
        )

    return quantity_on_hand, reorder_level


def generate_inventory(
    product_dataframe: pd.DataFrame,
    location_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Generate RetailNova current inventory."""

    inventory_count = config.get_record_count(
        "inventory_records"
    )

    product_ids = (
        product_dataframe["product_id"]
        .astype(int)
        .tolist()
    )

    location_ids = (
        location_dataframe["location_id"]
        .astype(int)
        .tolist()
    )

    location_type_lookup = dict(
        zip(
            location_dataframe[
                "location_id"
            ].astype(int),
            location_dataframe["location_type"],
        )
    )

    rng = set_random_seeds(config.random_seed + 3)

    inventory_pairs = select_inventory_pairs(
        product_ids,
        location_ids,
        inventory_count,
        rng,
    )

    stock_update_start_date = (
        config.simulation_end_date
        - timedelta(days=30)
    )

    records = []

    for inventory_id, (
        product_id,
        location_id,
    ) in enumerate(inventory_pairs, start=1):
        location_type = location_type_lookup[
            location_id
        ]

        quantity_on_hand, reorder_level = (
            generate_stock_values(
                location_type,
                rng,
            )
        )

        stock_update_date = random_date_between(
            stock_update_start_date,
            config.simulation_end_date,
            rng,
        )

        stock_update_hour = rng.randint(7, 22)
        stock_update_minute = rng.randint(0, 59)

        timestamp = (
            f"{stock_update_date} "
            f"{stock_update_hour:02d}:"
            f"{stock_update_minute:02d}:00+00:00"
        )

        records.append(
            {
                "inventory_id": inventory_id,
                "product_id": product_id,
                "location_id": location_id,
                "quantity_on_hand": quantity_on_hand,
                "reorder_level": reorder_level,
                "last_stock_update": timestamp,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
        )

    inventory_dataframe = pd.DataFrame(
        records,
        columns=INVENTORY_COLUMNS,
    )

    validate_inventory(
        inventory_dataframe,
        product_dataframe,
        location_dataframe,
        config,
    )

    return inventory_dataframe


def validate_inventory(
    dataframe: pd.DataFrame,
    product_dataframe: pd.DataFrame,
    location_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate inventory before export."""

    expected_count = config.get_record_count(
        "inventory_records"
    )

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} inventory records, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != INVENTORY_COLUMNS:
        raise ValueError(
            "Inventory column order does not match the "
            "PostgreSQL inventory table."
        )

    validate_primary_key(
        dataframe,
        "inventory_id",
        "inventory",
    )

    validate_not_null_columns(
        dataframe,
        INVENTORY_COLUMNS,
        "inventory",
    )

    validate_foreign_key(
        dataframe,
        "product_id",
        product_dataframe,
        "product_id",
        "inventory.product_id -> product.product_id",
    )

    validate_foreign_key(
        dataframe,
        "location_id",
        location_dataframe,
        "location_id",
        "inventory.location_id -> location.location_id",
    )

    validate_non_negative(
        dataframe,
        [
            "quantity_on_hand",
            "reorder_level",
        ],
        "inventory",
    )

    duplicate_pairs = dataframe.duplicated(
        subset=[
            "product_id",
            "location_id",
        ]
    )

    if duplicate_pairs.any():
        raise ValueError(
            "Duplicate product-location inventory "
            "combinations detected."
        )

    expected_products = set(
        product_dataframe["product_id"].astype(int)
    )

    inventory_products = set(
        dataframe["product_id"].astype(int)
    )

    if inventory_products != expected_products:
        raise ValueError(
            "Every product must have at least one "
            "inventory record."
        )

    expected_locations = set(
        location_dataframe[
            "location_id"
        ].astype(int)
    )

    inventory_locations = set(
        dataframe["location_id"].astype(int)
    )

    if inventory_locations != expected_locations:
        raise ValueError(
            "Every location must have at least one "
            "inventory record."
        )

    integer_columns = [
        "quantity_on_hand",
        "reorder_level",
    ]

    for column in integer_columns:
        if not dataframe[column].map(
            lambda value: isinstance(value, int)
        ).all():
            raise ValueError(
                f"inventory.{column} must contain integers."
            )


def export_inventory(
    dataframe: pd.DataFrame,
    product_dataframe: pd.DataFrame,
    location_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export inventory.csv."""

    validate_inventory(
        dataframe,
        product_dataframe,
        location_dataframe,
        config,
    )

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["inventory"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=INVENTORY_COLUMNS,
    )


def generate_and_export_inventory(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Generate and export inventory."""

    (
        product_dataframe,
        location_dataframe,
    ) = load_inventory_dependencies(config)

    inventory_dataframe = generate_inventory(
        product_dataframe,
        location_dataframe,
        config,
    )

    output_path = export_inventory(
        inventory_dataframe,
        product_dataframe,
        location_dataframe,
        config,
    )

    return inventory_dataframe, output_path


if __name__ == "__main__":
    inventory_df, csv_path = (
        generate_and_export_inventory()
    )

    print("Inventory generation completed.")
    print(
        dataframe_summary(
            inventory_df,
            "inventory",
        )
    )
    print(f"CSV: {csv_path}")
