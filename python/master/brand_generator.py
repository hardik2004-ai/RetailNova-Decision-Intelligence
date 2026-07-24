%%writefile /content/retailnova/python/master/brand_generator.py

"""
RetailNova Decision Intelligence Platform
Brand Master Data Generator

Generates the brand.csv dataset for the PostgreSQL
brand table.

Author: Hardik Narigra
"""

from pathlib import Path

import pandas as pd

try:
    from config import CONFIG, GeneratorConfig
    from constants import CSV_FILE_NAMES
    from utils import (
        dataframe_summary,
        export_dataframe,
        validate_not_null_columns,
        validate_primary_key,
    )
except ImportError as error:
    raise ImportError(
        "Unable to import RetailNova generator modules. "
        "Add /content/retailnova/python/generators to sys.path "
        "before importing brand_generator."
    ) from error


# =========================================================
# BRAND MASTER DATA
# =========================================================

BRAND_RECORDS = (
    (
        "Samsung",
        "Global consumer-electronics brand offering smartphones, "
        "televisions, appliances, wearables and smart-home devices.",
    ),
    (
        "Apple",
        "Premium technology brand offering smartphones, computers, "
        "tablets, wearables and digital accessories.",
    ),
    (
        "Sony",
        "Consumer-electronics and entertainment brand offering "
        "televisions, audio equipment, cameras and gaming products.",
    ),
    (
        "LG",
        "Consumer-electronics and home-appliance brand offering "
        "televisions, refrigerators, washing machines and monitors.",
    ),
    (
        "Xiaomi",
        "Technology brand offering smartphones, smart devices, "
        "wearables, televisions and connected-home products.",
    ),
    (
        "OnePlus",
        "Technology brand focused on smartphones, televisions, "
        "audio devices, tablets and mobile accessories.",
    ),
    (
        "Realme",
        "Consumer-technology brand offering smartphones, wearables, "
        "audio products and smart accessories.",
    ),
    (
        "Dell",
        "Computer-technology brand offering laptops, desktops, "
        "monitors, workstations and computing accessories.",
    ),
    (
        "HP",
        "Technology brand offering personal computers, printers, "
        "monitors and enterprise computing equipment.",
    ),
    (
        "Lenovo",
        "Global technology brand offering laptops, desktops, tablets, "
        "workstations and computing accessories.",
    ),
    (
        "Asus",
        "Computer-hardware brand offering laptops, gaming systems, "
        "components, monitors and networking products.",
    ),
    (
        "Acer",
        "Technology brand offering laptops, desktops, monitors, "
        "projectors and computing accessories.",
    ),
    (
        "boAt",
        "Indian consumer-electronics brand offering headphones, "
        "speakers, smartwatches and mobile accessories.",
    ),
    (
        "Philips",
        "Consumer and personal-care brand offering appliances, "
        "grooming products, lighting and healthcare devices.",
    ),
    (
        "Panasonic",
        "Consumer-electronics and appliance brand offering televisions, "
        "cameras, kitchen appliances and home equipment.",
    ),
    (
        "Whirlpool",
        "Home-appliance brand offering refrigerators, washing machines, "
        "air conditioners and kitchen appliances.",
    ),
    (
        "Bosch",
        "Engineering and appliance brand offering home appliances, "
        "power tools, automotive products and equipment.",
    ),
    (
        "Puma",
        "Sports and lifestyle brand offering footwear, apparel, "
        "sportswear and fashion accessories.",
    ),
    (
        "Adidas",
        "Global sportswear brand offering footwear, apparel, fitness "
        "products and sports accessories.",
    ),
    (
        "Nike",
        "Global athletic brand offering sports footwear, apparel, "
        "training equipment and lifestyle accessories.",
    ),
    (
        "Levi's",
        "Fashion brand known for denim apparel, casual clothing "
        "and lifestyle accessories.",
    ),
    (
        "Allen Solly",
        "Indian fashion brand offering formal, casual and contemporary "
        "apparel for men and women.",
    ),
    (
        "Lakmé",
        "Indian beauty brand offering cosmetics, skincare and "
        "personal-care products.",
    ),
    (
        "Mamaearth",
        "Indian personal-care brand offering skincare, haircare, "
        "beauty and wellness products.",
    ),
    (
        "L'Oréal Paris",
        "Global beauty brand offering skincare, cosmetics, haircare "
        "and personal-grooming products.",
    ),
    (
        "Himalaya",
        "Personal-care and wellness brand offering herbal skincare, "
        "haircare, healthcare and baby-care products.",
    ),
    (
        "Prestige",
        "Indian kitchen-appliance brand offering cookware, pressure "
        "cookers and small household appliances.",
    ),
    (
        "Pigeon",
        "Kitchen and home-appliance brand offering cookware, mixers, "
        "cooktops and household utility products.",
    ),
    (
        "Milton",
        "Indian household-products brand offering drinkware, "
        "food-storage containers and kitchen utilities.",
    ),
    (
        "Godrej Interio",
        "Indian furniture brand offering home, office and institutional "
        "furniture and storage solutions.",
    ),
    (
        "Nilkamal",
        "Indian furniture brand offering home furniture, office "
        "furniture, storage and material-handling products.",
    ),
    (
        "Decathlon",
        "Sports retailer and product brand offering equipment, apparel "
        "and accessories across multiple sporting categories.",
    ),
    (
        "Yonex",
        "Sports-equipment brand specializing in badminton, tennis "
        "and related athletic accessories.",
    ),
    (
        "Funskool",
        "Indian toy brand offering educational toys, games, puzzles "
        "and recreational products for children.",
    ),
    (
        "Penguin Random House",
        "Publishing brand offering fiction, non-fiction, educational "
        "and children's books.",
    ),
    (
        "Nestlé",
        "Global food and beverage brand offering packaged foods, "
        "nutrition products, beverages and confectionery.",
    ),
    (
        "Tata Consumer Products",
        "Indian consumer-products brand offering tea, coffee, packaged "
        "foods, beverages and everyday grocery products.",
    ),
)


BRAND_COLUMNS = [
    "brand_id",
    "brand_name",
    "description",
    "is_active",
    "created_at",
    "updated_at",
]


# Stable timestamp makes repeated generation reproducible.
MASTER_DATA_CREATED_AT = "2023-01-01 00:00:00+00:00"


# =========================================================
# GENERATOR
# =========================================================

def generate_brands(
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """
    Generate the RetailNova brand master dataset.

    Parameters
    ----------
    config:
        RetailNova generator configuration.

    Returns
    -------
    pandas.DataFrame
        Brand records matching the PostgreSQL brand table.
    """

    expected_count = config.get_record_count("brands")
    available_count = len(BRAND_RECORDS)

    if expected_count != available_count:
        raise ValueError(
            "Brand configuration mismatch: "
            f"configured={expected_count}, "
            f"available={available_count}."
        )

    records = []

    for brand_id, brand_data in enumerate(
        BRAND_RECORDS,
        start=1,
    ):
        brand_name, description = brand_data

        records.append(
            {
                "brand_id": brand_id,
                "brand_name": brand_name,
                "description": description,
                "is_active": True,
                "created_at": MASTER_DATA_CREATED_AT,
                "updated_at": MASTER_DATA_CREATED_AT,
            }
        )

    brand_dataframe = pd.DataFrame(
        records,
        columns=BRAND_COLUMNS,
    )

    validate_brands(brand_dataframe, config)

    return brand_dataframe


# =========================================================
# VALIDATION
# =========================================================

def validate_brands(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate brand data before CSV export."""

    expected_count = config.get_record_count("brands")

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} brands, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != BRAND_COLUMNS:
        raise ValueError(
            "Brand column order does not match the "
            "PostgreSQL brand table."
        )

    validate_primary_key(
        dataframe,
        "brand_id",
        "brand",
    )

    validate_not_null_columns(
        dataframe,
        [
            "brand_id",
            "brand_name",
            "is_active",
            "created_at",
            "updated_at",
        ],
        "brand",
    )

    if dataframe["brand_name"].duplicated().any():
        duplicate_names = (
            dataframe.loc[
                dataframe["brand_name"].duplicated(
                    keep=False
                ),
                "brand_name",
            ]
            .unique()
            .tolist()
        )

        raise ValueError(
            "brand_name must contain unique values. "
            f"Duplicates: {duplicate_names}"
        )

    if dataframe["brand_name"].str.strip().eq("").any():
        raise ValueError(
            "brand_name cannot contain empty values."
        )

    if (dataframe["brand_name"].str.len() > 100).any():
        raise ValueError(
            "brand_name exceeds VARCHAR(100)."
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

    if not dataframe["is_active"].map(
        lambda value: isinstance(value, bool)
    ).all():
        raise ValueError(
            "brand.is_active must contain Boolean values."
        )

    if not dataframe["is_active"].all():
        raise ValueError(
            "All initial brand records must be active."
        )


# =========================================================
# CSV EXPORT
# =========================================================

def export_brands(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export brand.csv."""

    validate_brands(dataframe, config)

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["brand"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=BRAND_COLUMNS,
    )


def generate_and_export_brands(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Generate, validate and export brand master data."""

    dataframe = generate_brands(config)
    output_path = export_brands(dataframe, config)

    return dataframe, output_path


if __name__ == "__main__":
    brand_df, csv_path = generate_and_export_brands()

    print("Brand generation completed.")
    print(dataframe_summary(brand_df, "brand"))
    print(f"CSV: {csv_path}")
