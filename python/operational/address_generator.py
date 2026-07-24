
"""
RetailNova Decision Intelligence Platform
Customer Address Data Generator

Generates address.csv using the customer master dataset.

Author: Hardik Narigra
"""

from pathlib import Path

import pandas as pd
from faker import Faker

try:
    from config import CONFIG, GeneratorConfig
    from constants import (
        COMPANY_COUNTRY,
        CSV_FILE_NAMES,
        INDIAN_CITIES,
        INDIAN_STATES,
    )
    from utils import (
        dataframe_summary,
        export_dataframe,
        set_random_seeds,
        validate_foreign_key,
        validate_not_null_columns,
        validate_primary_key,
        validate_required_columns,
    )
except ImportError as error:
    raise ImportError(
        "Unable to import RetailNova generator modules. "
        "Add /content/retailnova/python/generators to sys.path "
        "before importing address_generator."
    ) from error


ADDRESS_COLUMNS = [
    "address_id",
    "customer_id",
    "address_line_1",
    "address_line_2",
    "city",
    "state",
    "postal_code",
    "country",
    "is_default",
    "created_at",
    "updated_at",
]


CITY_LOCATIONS = (
    ("Mumbai", "Maharashtra", "400001"),
    ("Pune", "Maharashtra", "411001"),
    ("Thane", "Maharashtra", "400601"),
    ("Nashik", "Maharashtra", "422001"),
    ("Nagpur", "Maharashtra", "440001"),
    ("Ahmedabad", "Gujarat", "380001"),
    ("Surat", "Gujarat", "395001"),
    ("Vadodara", "Gujarat", "390001"),
    ("Bengaluru", "Karnataka", "560001"),
    ("Mysuru", "Karnataka", "570001"),
    ("Chennai", "Tamil Nadu", "600001"),
    ("Coimbatore", "Tamil Nadu", "641001"),
    ("Hyderabad", "Telangana", "500001"),
    ("New Delhi", "Delhi", "110001"),
    ("Kolkata", "West Bengal", "700001"),
    ("Jaipur", "Rajasthan", "302001"),
    ("Lucknow", "Uttar Pradesh", "226001"),
    ("Indore", "Madhya Pradesh", "452001"),
    ("Bhopal", "Madhya Pradesh", "462001"),
    ("Noida", "Uttar Pradesh", "201301"),
)


def load_customer_data(
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Load customer.csv for address generation."""

    customer_path = (
        config.output_directory
        / CSV_FILE_NAMES["customer"]
    )

    if not customer_path.exists():
        raise FileNotFoundError(
            f"Customer dataset not found: {customer_path}"
        )

    customer_dataframe = pd.read_csv(
        customer_path,
        dtype={"phone_number": str},
    )

    validate_required_columns(
        customer_dataframe,
        [
            "customer_id",
            "registration_date",
        ],
        "customer",
    )

    return customer_dataframe


def create_address_line_1(
    faker: Faker,
) -> str:
    """Create a compact Indian-style street address."""

    return (
        f"{faker.building_number()}, "
        f"{faker.street_name()}"
    )[:150]


def create_optional_address_line_2(
    rng,
) -> str | None:
    """Create an optional apartment or landmark value."""

    if rng.random() >= 0.45:
        return None

    options = [
        f"Apartment {rng.randint(1, 1204)}",
        f"Floor {rng.randint(1, 15)}",
        f"Block {rng.choice('ABCDEFGH')}",
        f"Near Sector {rng.randint(1, 90)} Market",
        f"Opposite Community Park {rng.randint(1, 20)}",
    ]

    return rng.choice(options)


def generate_addresses(
    customer_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Generate addresses for existing customers."""

    expected_address_count = config.get_record_count(
        "addresses"
    )

    customer_ids = (
        customer_dataframe["customer_id"]
        .astype(int)
        .tolist()
    )

    customer_count = len(customer_ids)

    if expected_address_count < customer_count:
        raise ValueError(
            "Address count cannot be lower than "
            "the number of customers."
        )

    additional_address_count = (
        expected_address_count - customer_count
    )

    if additional_address_count > customer_count:
        raise ValueError(
            "Current address model supports at most "
            "two addresses per customer."
        )

    rng = set_random_seeds(config.random_seed + 1)

    faker = Faker("en_IN")
    faker.seed_instance(config.random_seed + 1)

    customers_with_second_address = set(
        rng.sample(
            customer_ids,
            additional_address_count,
        )
    )

    registration_lookup = dict(
        zip(
            customer_dataframe["customer_id"].astype(int),
            customer_dataframe["registration_date"],
        )
    )

    records = []
    address_id = 1

    for customer_id in customer_ids:
        address_total = (
            2
            if customer_id in customers_with_second_address
            else 1
        )

        for customer_address_number in range(
            address_total
        ):
            city, state, postal_code = rng.choice(
                CITY_LOCATIONS
            )

            registration_date = registration_lookup[
                customer_id
            ]

            timestamp = (
                f"{registration_date} 00:00:00+00:00"
            )

            records.append(
                {
                    "address_id": address_id,
                    "customer_id": customer_id,
                    "address_line_1": (
                        create_address_line_1(faker)
                    ),
                    "address_line_2": (
                        create_optional_address_line_2(rng)
                    ),
                    "city": city,
                    "state": state,
                    "postal_code": postal_code,
                    "country": COMPANY_COUNTRY,
                    "is_default": (
                        customer_address_number == 0
                    ),
                    "created_at": timestamp,
                    "updated_at": timestamp,
                }
            )

            address_id += 1

    address_dataframe = pd.DataFrame(
        records,
        columns=ADDRESS_COLUMNS,
    )

    validate_addresses(
        address_dataframe,
        customer_dataframe,
        config,
    )

    return address_dataframe


def validate_addresses(
    dataframe: pd.DataFrame,
    customer_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate address records before export."""

    expected_count = config.get_record_count("addresses")

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} addresses, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != ADDRESS_COLUMNS:
        raise ValueError(
            "Address column order does not match the "
            "PostgreSQL address table."
        )

    validate_primary_key(
        dataframe,
        "address_id",
        "address",
    )

    validate_not_null_columns(
        dataframe,
        [
            "address_id",
            "customer_id",
            "address_line_1",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
            "created_at",
            "updated_at",
        ],
        "address",
    )

    validate_foreign_key(
        dataframe,
        "customer_id",
        customer_dataframe,
        "customer_id",
        "address.customer_id -> customer.customer_id",
    )

    customer_ids = set(
        customer_dataframe["customer_id"].astype(int)
    )

    addressed_customer_ids = set(
        dataframe["customer_id"].astype(int)
    )

    if addressed_customer_ids != customer_ids:
        missing_customers = (
            customer_ids - addressed_customer_ids
        )

        raise ValueError(
            "Every customer must have an address. "
            f"Missing customers: {missing_customers}"
        )

    default_counts = (
        dataframe.groupby("customer_id")["is_default"]
        .sum()
    )

    invalid_default_counts = default_counts[
        default_counts != 1
    ]

    if not invalid_default_counts.empty:
        raise ValueError(
            "Every customer must have exactly one "
            "default address."
        )

    address_counts = (
        dataframe.groupby("customer_id")
        .size()
    )

    if not address_counts.between(1, 2).all():
        raise ValueError(
            "Customers must have one or two addresses."
        )

    if not dataframe["is_default"].map(
        lambda value: isinstance(value, bool)
    ).all():
        raise ValueError(
            "address.is_default must contain Boolean values."
        )

    length_limits = {
        "address_line_1": 150,
        "address_line_2": 150,
        "city": 100,
        "state": 100,
        "postal_code": 20,
        "country": 100,
    }

    for column, maximum_length in length_limits.items():
        lengths = (
            dataframe[column]
            .fillna("")
            .astype(str)
            .str.len()
        )

        if lengths.gt(maximum_length).any():
            raise ValueError(
                f"address.{column} exceeds "
                f"VARCHAR({maximum_length})."
            )

    invalid_cities = (
        set(dataframe["city"])
        - set(INDIAN_CITIES)
    )

    if invalid_cities:
        raise ValueError(
            f"Unsupported address cities: {invalid_cities}"
        )

    invalid_states = (
        set(dataframe["state"])
        - set(INDIAN_STATES)
    )

    if invalid_states:
        raise ValueError(
            f"Unsupported address states: {invalid_states}"
        )

    invalid_postal_codes = dataframe.loc[
        ~dataframe["postal_code"].str.match(
            r"^[1-9]\d{5}$"
        ),
        "postal_code",
    ].tolist()

    if invalid_postal_codes:
        raise ValueError(
            "Invalid Indian postal codes: "
            f"{invalid_postal_codes[:5]}"
        )

    if not dataframe["country"].eq(
        COMPANY_COUNTRY
    ).all():
        raise ValueError(
            f"All addresses must use {COMPANY_COUNTRY}."
        )


def export_addresses(
    dataframe: pd.DataFrame,
    customer_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export address.csv."""

    validate_addresses(
        dataframe,
        customer_dataframe,
        config,
    )

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["address"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=ADDRESS_COLUMNS,
    )


def generate_and_export_addresses(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Load customers, generate and export addresses."""

    customer_dataframe = load_customer_data(config)

    address_dataframe = generate_addresses(
        customer_dataframe,
        config,
    )

    output_path = export_addresses(
        address_dataframe,
        customer_dataframe,
        config,
    )

    return address_dataframe, output_path


if __name__ == "__main__":
    address_df, csv_path = (
        generate_and_export_addresses()
    )

    print("Address generation completed.")
    print(dataframe_summary(address_df, "address"))
    print(f"CSV: {csv_path}")
