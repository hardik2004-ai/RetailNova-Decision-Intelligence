

"""
RetailNova Decision Intelligence Platform
Location Master Data Generator

Generates the location.csv dataset for RetailNova stores
and warehouses.

Author: Hardik Narigra
"""

import re
from pathlib import Path

import pandas as pd

try:
    from config import CONFIG, GeneratorConfig
    from constants import (
        COMPANY_COUNTRY,
        CSV_FILE_NAMES,
        INDIAN_CITIES,
        INDIAN_STATES,
        LOCATION_TYPES,
    )
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
        "Add /content/retailnova/python/generators to sys.path "
        "before importing location_generator."
    ) from error


# =========================================================
# LOCATION MASTER DATA
# =========================================================

LOCATION_RECORDS = (
    (
        "RetailNova Mumbai Andheri Store",
        "STORE",
        "Marol Main Road, Andheri East",
        "Mumbai",
        "Maharashtra",
        "400059",
        "9867000001",
    ),
    (
        "RetailNova Pune Baner Store",
        "STORE",
        "Baner High Street",
        "Pune",
        "Maharashtra",
        "411045",
        "9867000002",
    ),
    (
        "RetailNova Thane Store",
        "STORE",
        "Ghodbunder Road",
        "Thane",
        "Maharashtra",
        "400607",
        "9867000003",
    ),
    (
        "RetailNova Nashik Store",
        "STORE",
        "College Road",
        "Nashik",
        "Maharashtra",
        "422005",
        "9867000004",
    ),
    (
        "RetailNova Nagpur Store",
        "STORE",
        "Wardha Road",
        "Nagpur",
        "Maharashtra",
        "440015",
        "9867000005",
    ),
    (
        "RetailNova Ahmedabad Store",
        "STORE",
        "SG Highway",
        "Ahmedabad",
        "Gujarat",
        "380054",
        "9867000006",
    ),
    (
        "RetailNova Surat Store",
        "STORE",
        "Dumas Road",
        "Surat",
        "Gujarat",
        "395007",
        "9867000007",
    ),
    (
        "RetailNova Bengaluru Store",
        "STORE",
        "Whitefield Main Road",
        "Bengaluru",
        "Karnataka",
        "560066",
        "9867000008",
    ),
    (
        "RetailNova Mysuru Store",
        "STORE",
        "Vijayanagar Main Road",
        "Mysuru",
        "Karnataka",
        "570017",
        "9867000009",
    ),
    (
        "RetailNova Chennai Store",
        "STORE",
        "Anna Nagar Second Avenue",
        "Chennai",
        "Tamil Nadu",
        "600040",
        "9867000010",
    ),
    (
        "RetailNova Coimbatore Store",
        "STORE",
        "Avinashi Road",
        "Coimbatore",
        "Tamil Nadu",
        "641018",
        "9867000011",
    ),
    (
        "RetailNova Hyderabad Store",
        "STORE",
        "Hitech City Road",
        "Hyderabad",
        "Telangana",
        "500081",
        "9867000012",
    ),
    (
        "RetailNova New Delhi Store",
        "STORE",
        "Connaught Place",
        "New Delhi",
        "Delhi",
        "110001",
        "9867000013",
    ),
    (
        "RetailNova Kolkata Store",
        "STORE",
        "Salt Lake Sector I",
        "Kolkata",
        "West Bengal",
        "700064",
        "9867000014",
    ),
    (
        "RetailNova Jaipur Store",
        "STORE",
        "Malviya Nagar",
        "Jaipur",
        "Rajasthan",
        "302017",
        "9867000015",
    ),
    (
        "RetailNova Mumbai Regional Warehouse",
        "WAREHOUSE",
        "Taloja Industrial Area",
        "Mumbai",
        "Maharashtra",
        "410208",
        "9867000016",
    ),
    (
        "RetailNova Ahmedabad Regional Warehouse",
        "WAREHOUSE",
        "Sanand Industrial Estate",
        "Ahmedabad",
        "Gujarat",
        "382110",
        "9867000017",
    ),
    (
        "RetailNova Bengaluru Regional Warehouse",
        "WAREHOUSE",
        "Nelamangala Logistics Park",
        "Bengaluru",
        "Karnataka",
        "562123",
        "9867000018",
    ),
    (
        "RetailNova Hyderabad Regional Warehouse",
        "WAREHOUSE",
        "Shamshabad Logistics Zone",
        "Hyderabad",
        "Telangana",
        "501218",
        "9867000019",
    ),
    (
        "RetailNova Noida Regional Warehouse",
        "WAREHOUSE",
        "Sector 80 Industrial Area",
        "Noida",
        "Uttar Pradesh",
        "201305",
        "9867000020",
    ),
)


LOCATION_COLUMNS = [
    "location_id",
    "location_name",
    "location_type",
    "address",
    "city",
    "state",
    "country",
    "postal_code",
    "phone_number",
    "is_active",
    "created_at",
    "updated_at",
]


MASTER_DATA_CREATED_AT = "2023-01-01 00:00:00+00:00"

EXPECTED_STORE_COUNT = 15
EXPECTED_WAREHOUSE_COUNT = 5


# =========================================================
# GENERATOR
# =========================================================

def generate_locations(
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Generate RetailNova stores and warehouses."""

    expected_count = config.get_record_count("locations")
    available_count = len(LOCATION_RECORDS)

    if expected_count != available_count:
        raise ValueError(
            "Location configuration mismatch: "
            f"configured={expected_count}, "
            f"available={available_count}."
        )

    records = []

    for location_id, location_data in enumerate(
        LOCATION_RECORDS,
        start=1,
    ):
        (
            location_name,
            location_type,
            address,
            city,
            state,
            postal_code,
            phone_number,
        ) = location_data

        records.append(
            {
                "location_id": location_id,
                "location_name": location_name,
                "location_type": location_type,
                "address": address,
                "city": city,
                "state": state,
                "country": COMPANY_COUNTRY,
                "postal_code": postal_code,
                "phone_number": phone_number,
                "is_active": True,
                "created_at": MASTER_DATA_CREATED_AT,
                "updated_at": MASTER_DATA_CREATED_AT,
            }
        )

    location_dataframe = pd.DataFrame(
        records,
        columns=LOCATION_COLUMNS,
    )

    validate_locations(location_dataframe, config)

    return location_dataframe


# =========================================================
# VALIDATION
# =========================================================

def validate_locations(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate location data before CSV export."""

    expected_count = config.get_record_count("locations")

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} locations, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != LOCATION_COLUMNS:
        raise ValueError(
            "Location column order does not match the "
            "PostgreSQL location table."
        )

    validate_primary_key(
        dataframe,
        "location_id",
        "location",
    )

    validate_not_null_columns(
        dataframe,
        LOCATION_COLUMNS,
        "location",
    )

    validate_allowed_values(
        dataframe,
        "location_type",
        LOCATION_TYPES,
        "location",
    )

    if dataframe["location_name"].duplicated().any():
        raise ValueError(
            "location_name must contain unique values."
        )

    if dataframe["phone_number"].duplicated().any():
        raise ValueError(
            "location phone numbers must be unique."
        )

    location_type_counts = (
        dataframe["location_type"]
        .value_counts()
        .to_dict()
    )

    if location_type_counts.get("STORE", 0) != EXPECTED_STORE_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_STORE_COUNT} stores, found "
            f"{location_type_counts.get('STORE', 0)}."
        )

    if (
        location_type_counts.get("WAREHOUSE", 0)
        != EXPECTED_WAREHOUSE_COUNT
    ):
        raise ValueError(
            f"Expected {EXPECTED_WAREHOUSE_COUNT} warehouses, found "
            f"{location_type_counts.get('WAREHOUSE', 0)}."
        )

    length_limits = {
        "location_name": 150,
        "address": 255,
        "city": 100,
        "state": 100,
        "country": 100,
        "postal_code": 20,
        "phone_number": 20,
    }

    for column, maximum_length in length_limits.items():
        if (
            dataframe[column]
            .astype(str)
            .str.len()
            .gt(maximum_length)
            .any()
        ):
            raise ValueError(
                f"location.{column} exceeds "
                f"VARCHAR({maximum_length})."
            )

    invalid_cities = (
        set(dataframe["city"])
        - set(INDIAN_CITIES)
    )

    if invalid_cities:
        raise ValueError(
            f"Unsupported location cities: {invalid_cities}"
        )

    invalid_states = (
        set(dataframe["state"])
        - set(INDIAN_STATES)
    )

    if invalid_states:
        raise ValueError(
            f"Unsupported location states: {invalid_states}"
        )

    if not dataframe["country"].eq(
        COMPANY_COUNTRY
    ).all():
        raise ValueError(
            f"All locations must use country={COMPANY_COUNTRY}."
        )

    invalid_phones = dataframe.loc[
        ~dataframe["phone_number"].str.match(r"^[6-9]\d{9}$"),
        "phone_number",
    ].tolist()

    if invalid_phones:
        raise ValueError(
            f"Invalid Indian phone numbers: {invalid_phones}"
        )

    postal_code_pattern = re.compile(r"^[1-9]\d{5}$")

    invalid_postal_codes = dataframe.loc[
        ~dataframe["postal_code"].str.match(
            postal_code_pattern
        ),
        "postal_code",
    ].tolist()

    if invalid_postal_codes:
        raise ValueError(
            f"Invalid Indian postal codes: {invalid_postal_codes}"
        )

    if not dataframe["is_active"].map(
        lambda value: isinstance(value, bool)
    ).all():
        raise ValueError(
            "location.is_active must contain Boolean values."
        )

    if not dataframe["is_active"].all():
        raise ValueError(
            "All initial locations must be active."
        )


# =========================================================
# CSV EXPORT
# =========================================================

def export_locations(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export location.csv."""

    validate_locations(dataframe, config)

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["location"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=LOCATION_COLUMNS,
    )


def generate_and_export_locations(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Generate, validate and export location data."""

    dataframe = generate_locations(config)
    output_path = export_locations(dataframe, config)

    return dataframe, output_path


if __name__ == "__main__":
    location_df, csv_path = (
        generate_and_export_locations()
    )

    print("Location generation completed.")
    print(dataframe_summary(location_df, "location"))
    print(f"CSV: {csv_path}")
