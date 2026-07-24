
"""
RetailNova Decision Intelligence Platform
Product Data Generator

Generates product.csv using category, brand and supplier
master datasets.

Author: Hardik Narigra
"""

from decimal import Decimal
from pathlib import Path

import pandas as pd

try:
    from business_rules import (
        CATEGORY_MARGIN_RANGES,
        calculate_selling_price,
        round_currency,
    )
    from config import CONFIG, GeneratorConfig
    from constants import CSV_FILE_NAMES
    from utils import (
        dataframe_summary,
        export_dataframe,
        generate_barcode,
        generate_sku,
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
        "before importing product_generator."
    ) from error


# =========================================================
# PRODUCT BLUEPRINTS
# =========================================================

# category, brand, product name, cost price

PRODUCT_BLUEPRINTS = (
    # Electronics
    ("Electronics", "Samsung", "Samsung 55-Inch Smart Television", 34500),
    ("Electronics", "Sony", "Sony Wireless Noise-Cancelling Headphones", 11200),
    ("Electronics", "LG", "LG Ultra-HD Smart Monitor", 23800),

    # Fashion
    ("Fashion", "Puma", "Puma Everyday Running Shoes", 2100),
    ("Fashion", "Adidas", "Adidas Performance Track Jacket", 1900),
    ("Fashion", "Nike", "Nike Lightweight Training Shoes", 2600),
    ("Fashion", "Levi's", "Levi's Classic Straight-Fit Jeans", 1750),

    # Home & Kitchen
    ("Home & Kitchen", "Prestige", "Prestige Stainless Steel Pressure Cooker", 1650),
    ("Home & Kitchen", "Pigeon", "Pigeon Multi-Purpose Mixer Grinder", 2200),
    ("Home & Kitchen", "Milton", "Milton Insulated Water Bottle Set", 650),
    ("Home & Kitchen", "Philips", "Philips Digital Air Fryer", 6200),

    # Beauty & Personal Care
    ("Beauty & Personal Care", "Lakmé", "Lakmé Matte Finish Lip Colour", 320),
    ("Beauty & Personal Care", "Mamaearth", "Mamaearth Natural Face Wash", 260),
    ("Beauty & Personal Care", "L'Oréal Paris", "L'Oréal Paris Repair Hair Serum", 480),
    ("Beauty & Personal Care", "Himalaya", "Himalaya Herbal Anti-Dandruff Shampoo", 210),

    # Sports & Fitness
    ("Sports & Fitness", "Decathlon", "Decathlon Non-Slip Yoga Mat", 720),
    ("Sports & Fitness", "Yonex", "Yonex Lightweight Badminton Racquet", 1850),
    ("Sports & Fitness", "Puma", "Puma Training Gym Duffel Bag", 1400),

    # Books
    ("Books", "Penguin Random House", "Contemporary Business Analytics Handbook", 520),
    ("Books", "Penguin Random House", "Children's Illustrated Story Collection", 390),

    # Furniture
    ("Furniture", "Godrej Interio", "Godrej Interio Ergonomic Office Chair", 8500),
    ("Furniture", "Nilkamal", "Nilkamal Three-Door Storage Cabinet", 7100),
    ("Furniture", "Godrej Interio", "Godrej Interio Compact Study Desk", 6300),

    # Toys & Games
    ("Toys & Games", "Funskool", "Funskool Family Strategy Board Game", 780),
    ("Toys & Games", "Funskool", "Funskool Educational Building Blocks", 620),

    # Grocery
    ("Grocery", "Nestlé", "Nestlé Premium Instant Coffee", 340),
    ("Grocery", "Nestlé", "Nestlé Whole-Grain Breakfast Cereal", 280),
    ("Grocery", "Tata Consumer Products", "Tata Premium Assam Tea", 240),
    ("Grocery", "Tata Consumer Products", "Tata Iodised Everyday Salt", 28),

    # Smart Home
    ("Smart Home", "Xiaomi", "Xiaomi Smart Home Security Camera", 2250),
    ("Smart Home", "Samsung", "Samsung Connected Home Control Hub", 4800),
    ("Smart Home", "Philips", "Philips Wi-Fi Smart LED Bulb", 720),

    # Mobiles & Accessories
    ("Mobiles & Accessories", "Apple", "Apple Premium Smartphone 128GB", 61000),
    ("Mobiles & Accessories", "Samsung", "Samsung 5G Smartphone 128GB", 24500),
    ("Mobiles & Accessories", "OnePlus", "OnePlus Performance Smartphone 256GB", 29500),
    ("Mobiles & Accessories", "Realme", "Realme Budget 5G Smartphone 128GB", 12800),

    # Computers & Laptops
    ("Computers & Laptops", "Dell", "Dell Business Laptop 15-Inch", 42500),
    ("Computers & Laptops", "HP", "HP Everyday Productivity Laptop", 39800),
    ("Computers & Laptops", "Lenovo", "Lenovo Professional Think-Series Laptop", 46500),
    ("Computers & Laptops", "Asus", "Asus Performance Gaming Laptop", 68500),
    ("Computers & Laptops", "Acer", "Acer Lightweight Student Laptop", 33500),

    # Appliances
    ("Appliances", "Whirlpool", "Whirlpool Double-Door Refrigerator", 24500),
    ("Appliances", "LG", "LG Front-Load Washing Machine", 28500),
    ("Appliances", "Panasonic", "Panasonic Convection Microwave Oven", 8900),
    ("Appliances", "Bosch", "Bosch Automatic Dishwasher", 36500),

    # Automotive
    ("Automotive", "Bosch", "Bosch Portable Tyre Inflator", 2650),
    ("Automotive", "Philips", "Philips Compact Car Vacuum Cleaner", 2100),

    # Office Supplies
    ("Office Supplies", "HP", "HP Wireless Office Keyboard and Mouse", 1450),
    ("Office Supplies", "Dell", "Dell Professional Laptop Backpack", 1750),
    ("Office Supplies", "Milton", "Milton Desktop Organisation Set", 560),
)


PRODUCT_COLUMNS = [
    "product_id",
    "category_id",
    "brand_id",
    "supplier_id",
    "product_name",
    "sku",
    "barcode",
    "description",
    "unit_price",
    "cost_price",
    "is_active",
    "created_at",
    "updated_at",
]


MASTER_DATA_CREATED_AT = "2023-01-01 00:00:00+00:00"


# =========================================================
# MASTER DATA LOADING
# =========================================================

def load_product_dependencies(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load category, brand and supplier master datasets."""

    category_path = (
        config.output_directory
        / CSV_FILE_NAMES["category"]
    )

    brand_path = (
        config.output_directory
        / CSV_FILE_NAMES["brand"]
    )

    supplier_path = (
        config.output_directory
        / CSV_FILE_NAMES["supplier"]
    )

    required_paths = [
        category_path,
        brand_path,
        supplier_path,
    ]

    missing_files = [
        str(path)
        for path in required_paths
        if not path.exists()
    ]

    if missing_files:
        raise FileNotFoundError(
            "Product dependencies are missing: "
            f"{missing_files}"
        )

    category_dataframe = pd.read_csv(category_path)
    brand_dataframe = pd.read_csv(brand_path)
    supplier_dataframe = pd.read_csv(supplier_path)

    validate_required_columns(
        category_dataframe,
        ["category_id", "category_name"],
        "category",
    )

    validate_required_columns(
        brand_dataframe,
        ["brand_id", "brand_name"],
        "brand",
    )

    validate_required_columns(
        supplier_dataframe,
        ["supplier_id", "supplier_name"],
        "supplier",
    )

    return (
        category_dataframe,
        brand_dataframe,
        supplier_dataframe,
    )


# =========================================================
# GENERATOR
# =========================================================

def generate_products(
    category_dataframe: pd.DataFrame,
    brand_dataframe: pd.DataFrame,
    supplier_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Generate the RetailNova product dataset."""

    expected_count = config.get_record_count("products")
    available_count = len(PRODUCT_BLUEPRINTS)

    if expected_count != available_count:
        raise ValueError(
            "Product configuration mismatch: "
            f"configured={expected_count}, "
            f"available={available_count}."
        )

    rng = set_random_seeds(config.random_seed)

    category_lookup = dict(
        zip(
            category_dataframe["category_name"],
            category_dataframe["category_id"],
        )
    )

    brand_lookup = dict(
        zip(
            brand_dataframe["brand_name"],
            brand_dataframe["brand_id"],
        )
    )

    supplier_ids = (
        supplier_dataframe["supplier_id"]
        .astype(int)
        .tolist()
    )

    rng.shuffle(supplier_ids)

    records = []

    for product_id, blueprint in enumerate(
        PRODUCT_BLUEPRINTS,
        start=1,
    ):
        (
            category_name,
            brand_name,
            product_name,
            base_cost_price,
        ) = blueprint

        if category_name not in category_lookup:
            raise ValueError(
                f"Unknown product category: {category_name}"
            )

        if brand_name not in brand_lookup:
            raise ValueError(
                f"Unknown product brand: {brand_name}"
            )

        margin_minimum, margin_maximum = (
            CATEGORY_MARGIN_RANGES[category_name]
        )

        # calculate_selling_price requires at least 10% markup.
        effective_minimum = max(10.0, margin_minimum)

        markup_percentage = round(
            rng.uniform(
                effective_minimum,
                margin_maximum,
            ),
            2,
        )

        cost_price = round_currency(base_cost_price)

        unit_price = calculate_selling_price(
            cost_price,
            markup_percentage,
        )

        category_code = category_name[:4]
        brand_code = brand_name[:4]

        sku = generate_sku(
            category_code,
            brand_code,
            product_id,
        )

        barcode = generate_barcode(product_id)

        supplier_id = supplier_ids[
            (product_id - 1) % len(supplier_ids)
        ]

        description = (
            f"{product_name} supplied through RetailNova's "
            f"{category_name} product portfolio."
        )

        records.append(
            {
                "product_id": product_id,
                "category_id": int(
                    category_lookup[category_name]
                ),
                "brand_id": int(
                    brand_lookup[brand_name]
                ),
                "supplier_id": int(supplier_id),
                "product_name": product_name,
                "sku": sku,
                "barcode": barcode,
                "description": description,
                "unit_price": unit_price,
                "cost_price": cost_price,
                "is_active": True,
                "created_at": MASTER_DATA_CREATED_AT,
                "updated_at": MASTER_DATA_CREATED_AT,
            }
        )

    product_dataframe = pd.DataFrame(
        records,
        columns=PRODUCT_COLUMNS,
    )

    validate_products(
        product_dataframe,
        category_dataframe,
        brand_dataframe,
        supplier_dataframe,
        config,
    )

    return product_dataframe


# =========================================================
# VALIDATION
# =========================================================

def validate_products(
    dataframe: pd.DataFrame,
    category_dataframe: pd.DataFrame,
    brand_dataframe: pd.DataFrame,
    supplier_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate products before CSV export."""

    expected_count = config.get_record_count("products")

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} products, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != PRODUCT_COLUMNS:
        raise ValueError(
            "Product column order does not match the "
            "PostgreSQL product table."
        )

    validate_primary_key(
        dataframe,
        "product_id",
        "product",
    )

    validate_not_null_columns(
        dataframe,
        PRODUCT_COLUMNS,
        "product",
    )

    validate_foreign_key(
        dataframe,
        "category_id",
        category_dataframe,
        "category_id",
        "product.category_id -> category.category_id",
    )

    validate_foreign_key(
        dataframe,
        "brand_id",
        brand_dataframe,
        "brand_id",
        "product.brand_id -> brand.brand_id",
    )

    validate_foreign_key(
        dataframe,
        "supplier_id",
        supplier_dataframe,
        "supplier_id",
        "product.supplier_id -> supplier.supplier_id",
    )

    validate_non_negative(
        dataframe,
        ["unit_price", "cost_price"],
        "product",
    )

    for column in [
        "product_name",
        "sku",
        "barcode",
    ]:
        if dataframe[column].duplicated().any():
            raise ValueError(
                f"product.{column} must contain unique values."
            )

    if (dataframe["product_name"].str.len() > 150).any():
        raise ValueError(
            "product_name exceeds VARCHAR(150)."
        )

    if (dataframe["sku"].str.len() > 50).any():
        raise ValueError(
            "sku exceeds VARCHAR(50)."
        )

    if (dataframe["barcode"].str.len() > 50).any():
        raise ValueError(
            "barcode exceeds VARCHAR(50)."
        )

    if (
        dataframe["description"]
        .fillna("")
        .str.len()
        .gt(500)
        .any()
    ):
        raise ValueError(
            "description exceeds VARCHAR(500)."
        )

    invalid_barcodes = dataframe.loc[
        ~dataframe["barcode"].str.match(r"^\d{13}$"),
        "barcode",
    ].tolist()

    if invalid_barcodes:
        raise ValueError(
            f"Invalid EAN-13 barcodes: {invalid_barcodes}"
        )

    price_comparison = (
        dataframe["unit_price"].map(Decimal)
        < dataframe["cost_price"].map(Decimal)
    )

    if price_comparison.any():
        raise ValueError(
            "unit_price cannot be lower than cost_price."
        )

    maximum_numeric_value = Decimal("99999999.99")

    for column in ["unit_price", "cost_price"]:
        if dataframe[column].map(
            Decimal
        ).gt(maximum_numeric_value).any():
            raise ValueError(
                f"product.{column} exceeds NUMERIC(10,2)."
            )

    if not dataframe["is_active"].map(
        lambda value: isinstance(value, bool)
    ).all():
        raise ValueError(
            "product.is_active must contain Boolean values."
        )


# =========================================================
# CSV EXPORT
# =========================================================

def export_products(
    dataframe: pd.DataFrame,
    category_dataframe: pd.DataFrame,
    brand_dataframe: pd.DataFrame,
    supplier_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export product.csv."""

    validate_products(
        dataframe,
        category_dataframe,
        brand_dataframe,
        supplier_dataframe,
        config,
    )

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["product"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=PRODUCT_COLUMNS,
    )


def generate_and_export_products(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Load dependencies, generate and export products."""

    (
        category_dataframe,
        brand_dataframe,
        supplier_dataframe,
    ) = load_product_dependencies(config)

    product_dataframe = generate_products(
        category_dataframe,
        brand_dataframe,
        supplier_dataframe,
        config,
    )

    output_path = export_products(
        product_dataframe,
        category_dataframe,
        brand_dataframe,
        supplier_dataframe,
        config,
    )

    return product_dataframe, output_path


if __name__ == "__main__":
    product_df, csv_path = (
        generate_and_export_products()
    )

    print("Product generation completed.")
    print(dataframe_summary(product_df, "product"))
    print(f"CSV: {csv_path}")
