%%writefile /content/retailnova/python/master/category_generator.py

"""
RetailNova Decision Intelligence Platform
Category Master Data Generator

Generates the category.csv dataset for the PostgreSQL
category table.

Author: Hardik Narigra
"""

from pathlib import Path

import pandas as pd

try:
    from config import CONFIG, GeneratorConfig
    from constants import CSV_FILE_NAMES, PRODUCT_CATEGORIES
    from utils import (
        dataframe_summary,
        export_dataframe,
        validate_allowed_values,
        validate_not_null_columns,
        validate_primary_key,
    )
except ImportError as error:
    raise ImportError(
        "Unable to import RetailNova generator modules. "
        "Add python/generators to sys.path before importing "
        "category_generator."
    ) from error


# =========================================================
# CATEGORY MASTER DATA
# =========================================================

CATEGORY_DESCRIPTIONS = {
    "Electronics": (
        "Consumer electronics, audio devices, cameras, "
        "wearables and electronic accessories."
    ),
    "Fashion": (
        "Apparel, footwear, fashion accessories and "
        "lifestyle products for all customer segments."
    ),
    "Home & Kitchen": (
        "Kitchenware, cookware, home utilities, decor and "
        "household essentials."
    ),
    "Beauty & Personal Care": (
        "Skincare, haircare, grooming, cosmetics and "
        "personal-hygiene products."
    ),
    "Sports & Fitness": (
        "Sports equipment, exercise accessories, fitness "
        "products and outdoor essentials."
    ),
    "Books": (
        "Fiction, non-fiction, academic, professional and "
        "children's books."
    ),
    "Furniture": (
        "Residential and office furniture, storage units "
        "and home-furnishing products."
    ),
    "Toys & Games": (
        "Educational toys, board games, puzzles and "
        "recreational products for children and families."
    ),
    "Grocery": (
        "Packaged foods, beverages, staples and everyday "
        "household grocery essentials."
    ),
    "Smart Home": (
        "Connected home devices, automation products, "
        "security systems and smart appliances."
    ),
    "Mobiles & Accessories": (
        "Smartphones, feature phones, chargers, cases, "
        "screen protectors and mobile accessories."
    ),
    "Computers & Laptops": (
        "Laptops, desktops, computer components, storage "
        "devices and computing accessories."
    ),
    "Appliances": (
        "Major and small home appliances for cooking, "
        "cleaning, cooling and daily household use."
    ),
    "Automotive": (
        "Vehicle accessories, maintenance products, tools "
        "and automotive care essentials."
    ),
    "Office Supplies": (
        "Stationery, office equipment, organizational "
        "supplies and workplace consumables."
    ),
}


CATEGORY_COLUMNS = [
    "category_id",
    "category_name",
    "description",
    "is_active",
    "created_at",
    "updated_at",
]


# A stable historical timestamp makes repeated generation reproducible.
MASTER_DATA_CREATED_AT = "2023-01-01 00:00:00+00:00"


# =========================================================
# GENERATOR
# =========================================================

def generate_categories(
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """
    Generate the RetailNova category master dataset.

    Parameters
    ----------
    config:
        RetailNova generator configuration.

    Returns
    -------
    pandas.DataFrame
        Category records matching the PostgreSQL category table.
    """

    expected_count = config.get_record_count("categories")
    available_count = len(PRODUCT_CATEGORIES)

    if expected_count != available_count:
        raise ValueError(
            "Category configuration mismatch: "
            f"configured={expected_count}, "
            f"available={available_count}."
        )

    if set(PRODUCT_CATEGORIES) != set(
        CATEGORY_DESCRIPTIONS
    ):
        missing_descriptions = (
            set(PRODUCT_CATEGORIES)
            - set(CATEGORY_DESCRIPTIONS)
        )

        extra_descriptions = (
            set(CATEGORY_DESCRIPTIONS)
            - set(PRODUCT_CATEGORIES)
        )

        raise ValueError(
            "Category description mapping does not match "
            f"PRODUCT_CATEGORIES. Missing={missing_descriptions}, "
            f"extra={extra_descriptions}."
        )

    records = []

    for category_id, category_name in enumerate(
        PRODUCT_CATEGORIES,
        start=1,
    ):
        records.append(
            {
                "category_id": category_id,
                "category_name": category_name,
                "description": (
                    CATEGORY_DESCRIPTIONS[category_name]
                ),
                "is_active": True,
                "created_at": MASTER_DATA_CREATED_AT,
                "updated_at": MASTER_DATA_CREATED_AT,
            }
        )

    category_dataframe = pd.DataFrame(
        records,
        columns=CATEGORY_COLUMNS,
    )

    validate_categories(category_dataframe, config)

    return category_dataframe


# =========================================================
# VALIDATION
# =========================================================

def validate_categories(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate category data before CSV export."""

    expected_count = config.get_record_count("categories")

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} categories, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != CATEGORY_COLUMNS:
        raise ValueError(
            "Category column order does not match the "
            "PostgreSQL category table."
        )

    validate_primary_key(
        dataframe,
        "category_id",
        "category",
    )

    validate_not_null_columns(
        dataframe,
        [
            "category_id",
            "category_name",
            "is_active",
            "created_at",
            "updated_at",
        ],
        "category",
    )

    if dataframe["category_name"].duplicated().any():
        raise ValueError(
            "category_name must contain unique values."
        )

    validate_allowed_values(
        dataframe,
        "category_name",
        PRODUCT_CATEGORIES,
        "category",
    )

    if not dataframe["is_active"].map(
        lambda value: isinstance(value, bool)
    ).all():
        raise ValueError(
            "category.is_active must contain Boolean values."
        )

    if not dataframe["is_active"].all():
        raise ValueError(
            "All initial category records must be active."
        )

    if (
        dataframe["category_name"].str.len() > 100
    ).any():
        raise ValueError(
            "category_name exceeds VARCHAR(100)."
        )

    description_lengths = (
        dataframe["description"]
        .fillna("")
        .str.len()
    )

    if (description_lengths > 500).any():
        raise ValueError(
            "description exceeds VARCHAR(500)."
        )


# =========================================================
# CSV EXPORT
# =========================================================

def export_categories(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export category.csv."""

    validate_categories(dataframe, config)

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["category"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=CATEGORY_COLUMNS,
    )


def generate_and_export_categories(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Generate, validate and export category master data."""

    dataframe = generate_categories(config)
    output_path = export_categories(dataframe, config)

    return dataframe, output_path


if __name__ == "__main__":
    category_df, csv_path = (
        generate_and_export_categories()
    )

    print("Category generation completed.")
    print(dataframe_summary(category_df, "category"))
    print(f"CSV: {csv_path}")
