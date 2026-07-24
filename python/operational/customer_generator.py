
"""
RetailNova Decision Intelligence Platform
Customer Data Generator

Generates synthetic Indian customer records matching the
PostgreSQL customer table.

Author: Hardik Narigra
"""

from datetime import timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

try:
    from config import CONFIG, GeneratorConfig
    from constants import (
        CSV_FILE_NAMES,
        CUSTOMER_GENDERS,
    )
    from probability_models import CUSTOMER_GENDER_WEIGHTS
    from utils import (
        dataframe_summary,
        export_dataframe,
        generate_email,
        generate_indian_phone_number,
        random_date_between,
        set_random_seeds,
        validate_allowed_values,
        validate_not_null_columns,
        validate_primary_key,
    )
except ImportError as error:
    raise ImportError(
        "Unable to import RetailNova generator modules. "
        "Add /content/retailnova/python/generators to sys.path "
        "before importing customer_generator."
    ) from error


CUSTOMER_COLUMNS = [
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "phone_number",
    "date_of_birth",
    "gender",
    "registration_date",
    "is_active",
    "created_at",
    "updated_at",
]


MINIMUM_CUSTOMER_AGE = 18
MAXIMUM_CUSTOMER_AGE = 75
ACTIVE_CUSTOMER_PROBABILITY = 0.93


def generate_unique_phone(
    existing_phones: set[str],
    rng,
) -> str:
    """Generate a unique Indian mobile number."""

    while True:
        phone_number = generate_indian_phone_number(rng)

        if phone_number not in existing_phones:
            existing_phones.add(phone_number)
            return phone_number


def generate_name(
    gender: str,
    faker: Faker,
    rng,
) -> tuple[str, str]:
    """Generate a name broadly consistent with gender."""

    if gender == "MALE":
        first_name = faker.first_name_male()

    elif gender == "FEMALE":
        first_name = faker.first_name_female()

    else:
        first_name = rng.choice(
            [
                faker.first_name_male(),
                faker.first_name_female(),
            ]
        )

    last_name = faker.last_name()

    return first_name.strip(), last_name.strip()


def generate_customers(
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Generate synthetic RetailNova customers."""

    customer_count = config.get_record_count("customers")

    rng = set_random_seeds(config.random_seed)

    faker = Faker("en_IN")
    faker.seed_instance(config.random_seed)

    gender_values = list(
        CUSTOMER_GENDER_WEIGHTS.keys()
    )

    gender_weights = list(
        CUSTOMER_GENDER_WEIGHTS.values()
    )

    existing_phones: set[str] = set()
    records = []

    for customer_id in range(1, customer_count + 1):
        gender = rng.choices(
            gender_values,
            weights=gender_weights,
            k=1,
        )[0]

        first_name, last_name = generate_name(
            gender,
            faker,
            rng,
        )

        email = generate_email(
            first_name,
            last_name,
            customer_id,
            domain="retailnova.example.com",
        )

        phone_number = generate_unique_phone(
            existing_phones,
            rng,
        )

        registration_date = random_date_between(
            config.simulation_start_date,
            config.simulation_end_date,
            rng,
        )

        oldest_birth_date = (
            registration_date
            - timedelta(
                days=int(
                    MAXIMUM_CUSTOMER_AGE * 365.25
                )
            )
        )

        youngest_birth_date = (
            registration_date
            - timedelta(
                days=int(
                    MINIMUM_CUSTOMER_AGE * 365.25
                )
            )
        )

        date_of_birth = random_date_between(
            oldest_birth_date,
            youngest_birth_date,
            rng,
        )

        is_active = (
            rng.random()
            < ACTIVE_CUSTOMER_PROBABILITY
        )

        created_at = (
            f"{registration_date} 00:00:00+00:00"
        )

        records.append(
            {
                "customer_id": customer_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone_number": phone_number,
                "date_of_birth": date_of_birth,
                "gender": gender,
                "registration_date": registration_date,
                "is_active": is_active,
                "created_at": created_at,
                "updated_at": created_at,
            }
        )

    customer_dataframe = pd.DataFrame(
        records,
        columns=CUSTOMER_COLUMNS,
    )

    validate_customers(
        customer_dataframe,
        config,
    )

    return customer_dataframe


def validate_customers(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate customer data before export."""

    expected_count = config.get_record_count("customers")

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} customers, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != CUSTOMER_COLUMNS:
        raise ValueError(
            "Customer column order does not match the "
            "PostgreSQL customer table."
        )

    validate_primary_key(
        dataframe,
        "customer_id",
        "customer",
    )

    validate_not_null_columns(
        dataframe,
        CUSTOMER_COLUMNS,
        "customer",
    )

    validate_allowed_values(
        dataframe,
        "gender",
        CUSTOMER_GENDERS,
        "customer",
    )

    for column in ["email", "phone_number"]:
        if dataframe[column].duplicated().any():
            raise ValueError(
                f"customer.{column} must be unique."
            )

    length_limits = {
        "first_name": 50,
        "last_name": 50,
        "email": 255,
        "phone_number": 15,
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
                f"customer.{column} exceeds "
                f"VARCHAR({maximum_length})."
            )

    invalid_emails = dataframe.loc[
        ~dataframe["email"].str.match(
            r"^[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        ),
        "email",
    ].tolist()

    if invalid_emails:
        raise ValueError(
            f"Invalid customer emails: {invalid_emails[:5]}"
        )

    invalid_phones = dataframe.loc[
        ~dataframe["phone_number"].str.match(
            r"^[6-9]\d{9}$"
        ),
        "phone_number",
    ].tolist()

    if invalid_phones:
        raise ValueError(
            f"Invalid customer phones: {invalid_phones[:5]}"
        )

    birth_dates = pd.to_datetime(
        dataframe["date_of_birth"]
    )

    registration_dates = pd.to_datetime(
        dataframe["registration_date"]
    )

    ages = (
        registration_dates - birth_dates
    ).dt.days / 365.25

    if (
        (ages < MINIMUM_CUSTOMER_AGE)
        | (ages > MAXIMUM_CUSTOMER_AGE)
    ).any():
        raise ValueError(
            "Customer ages must be between "
            f"{MINIMUM_CUSTOMER_AGE} and "
            f"{MAXIMUM_CUSTOMER_AGE} at registration."
        )

    if (
        registration_dates.dt.date
        < config.simulation_start_date
    ).any():
        raise ValueError(
            "registration_date precedes the simulation."
        )

    if (
        registration_dates.dt.date
        > config.simulation_end_date
    ).any():
        raise ValueError(
            "registration_date exceeds the simulation."
        )

    if not dataframe["is_active"].map(
        lambda value: isinstance(value, bool)
    ).all():
        raise ValueError(
            "customer.is_active must contain Boolean values."
        )


def export_customers(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export customer.csv."""

    validate_customers(dataframe, config)

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["customer"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=CUSTOMER_COLUMNS,
    )


def generate_and_export_customers(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Generate, validate and export customers."""

    dataframe = generate_customers(config)
    output_path = export_customers(
        dataframe,
        config,
    )

    return dataframe, output_path


if __name__ == "__main__":
    customer_df, csv_path = (
        generate_and_export_customers()
    )

    print("Customer generation completed.")
    print(dataframe_summary(customer_df, "customer"))
    print(f"CSV: {csv_path}")
