%%writefile /content/retailnova/python/generators/utils.py

"""
RetailNova Decision Intelligence Platform
Synthetic Data Engine Utilities

Shared utilities for reproducible random generation, UUIDs,
dates, identifiers, validation, CSV export and logging.

Author: Hardik Narigra
"""

import logging
import random
import re
import string
import uuid
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any, Iterable, Sequence

import numpy as np
import pandas as pd

try:
    from .constants import DATE_FORMAT, TIMESTAMP_FORMAT
except ImportError:
    from constants import DATE_FORMAT, TIMESTAMP_FORMAT


# =========================================================
# REPRODUCIBILITY
# =========================================================

def set_random_seeds(seed: int) -> random.Random:
    """
    Seed Python and NumPy random generators.

    Returns an independent Python Random instance for use by
    generator functions.
    """

    if not isinstance(seed, int):
        raise TypeError("seed must be an integer.")

    if seed < 0:
        raise ValueError("seed cannot be negative.")

    random.seed(seed)
    np.random.seed(seed)

    return random.Random(seed)


# =========================================================
# DIRECTORY AND LOGGING UTILITIES
# =========================================================

def ensure_directory(directory: str | Path) -> Path:
    """Create a directory when it does not already exist."""

    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)

    return path


def configure_logger(
    name: str,
    log_directory: str | Path,
    level: int = logging.INFO,
) -> logging.Logger:
    """Create a console and file logger without duplicate handlers."""

    if not name.strip():
        raise ValueError("Logger name cannot be empty.")

    directory = ensure_directory(log_directory)
    log_file = directory / f"{name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt=TIMESTAMP_FORMAT,
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# =========================================================
# UUID AND IDENTIFIER UTILITIES
# =========================================================

def generate_uuid(
    rng: random.Random | None = None,
) -> str:
    """
    Generate a UUID4-compatible identifier.

    Supplying a seeded Random instance makes generation reproducible.
    """

    if rng is None:
        return str(uuid.uuid4())

    random_bits = rng.getrandbits(128)

    # Set UUID version to 4.
    random_bits &= ~(0xF << 76)
    random_bits |= 4 << 76

    # Set the RFC 4122 variant.
    random_bits &= ~(0x3 << 62)
    random_bits |= 0x2 << 62

    return str(uuid.UUID(int=random_bits))


def generate_uuid_batch(
    count: int,
    rng: random.Random | None = None,
) -> list[str]:
    """Generate a list of unique UUID strings."""

    if count < 0:
        raise ValueError("count cannot be negative.")

    random_generator = rng or random.Random()

    identifiers = [
        generate_uuid(random_generator)
        for _ in range(count)
    ]

    if len(identifiers) != len(set(identifiers)):
        raise RuntimeError(
            "Duplicate UUIDs were unexpectedly generated."
        )

    return identifiers


def generate_sequential_code(
    prefix: str,
    sequence_number: int,
    width: int = 8,
) -> str:
    """Create a readable business identifier."""

    normalized_prefix = prefix.strip().upper()

    if not normalized_prefix:
        raise ValueError("prefix cannot be empty.")

    if sequence_number <= 0:
        raise ValueError(
            "sequence_number must be greater than zero."
        )

    if width <= 0:
        raise ValueError("width must be greater than zero.")

    return f"{normalized_prefix}-{sequence_number:0{width}d}"


def generate_sku(
    category_code: str,
    brand_code: str,
    sequence_number: int,
) -> str:
    """Generate a RetailNova product SKU."""

    category = re.sub(
        r"[^A-Z0-9]",
        "",
        category_code.upper(),
    )[:4]

    brand = re.sub(
        r"[^A-Z0-9]",
        "",
        brand_code.upper(),
    )[:4]

    if not category or not brand:
        raise ValueError(
            "category_code and brand_code must contain "
            "alphanumeric characters."
        )

    if sequence_number <= 0:
        raise ValueError(
            "sequence_number must be greater than zero."
        )

    return f"RN-{category}-{brand}-{sequence_number:06d}"


def generate_barcode(
    sequence_number: int,
    prefix: str = "890",
) -> str:
    """
    Generate a deterministic 13-digit EAN-style barcode.

    The final digit is an EAN-13 check digit.
    """

    if sequence_number <= 0:
        raise ValueError(
            "sequence_number must be greater than zero."
        )

    if not prefix.isdigit():
        raise ValueError("prefix must contain only digits.")

    if len(prefix) >= 12:
        raise ValueError(
            "prefix must contain fewer than 12 digits."
        )

    available_width = 12 - len(prefix)

    body = (
        prefix
        + str(sequence_number).zfill(available_width)[
            -available_width:
        ]
    )

    digits = [int(character) for character in body]

    check_sum = sum(digits[::2]) + 3 * sum(digits[1::2])
    check_digit = (10 - check_sum % 10) % 10

    return body + str(check_digit)


# =========================================================
# DATE AND TIME UTILITIES
# =========================================================

def random_date_between(
    start_date: date,
    end_date: date,
    rng: random.Random | None = None,
) -> date:
    """Generate a random date within an inclusive range."""

    if not isinstance(start_date, date):
        raise TypeError("start_date must be a date.")

    if not isinstance(end_date, date):
        raise TypeError("end_date must be a date.")

    if start_date > end_date:
        raise ValueError(
            "start_date cannot be later than end_date."
        )

    random_generator = rng or random

    number_of_days = (end_date - start_date).days

    return start_date + timedelta(
        days=random_generator.randint(0, number_of_days)
    )


def random_datetime_between(
    start_datetime: datetime,
    end_datetime: datetime,
    rng: random.Random | None = None,
) -> datetime:
    """Generate a random datetime within an inclusive range."""

    if not isinstance(start_datetime, datetime):
        raise TypeError(
            "start_datetime must be a datetime."
        )

    if not isinstance(end_datetime, datetime):
        raise TypeError(
            "end_datetime must be a datetime."
        )

    if start_datetime > end_datetime:
        raise ValueError(
            "start_datetime cannot be later than end_datetime."
        )

    random_generator = rng or random

    total_seconds = int(
        (end_datetime - start_datetime).total_seconds()
    )

    random_seconds = random_generator.randint(
        0,
        total_seconds,
    )

    return start_datetime + timedelta(
        seconds=random_seconds
    )


def date_to_business_datetime(
    target_date: date,
    rng: random.Random | None = None,
    start_hour: int = 8,
    end_hour: int = 22,
) -> datetime:
    """Attach a realistic retail business time to a date."""

    if not isinstance(target_date, date):
        raise TypeError("target_date must be a date.")

    if not 0 <= start_hour <= 23:
        raise ValueError(
            "start_hour must be between 0 and 23."
        )

    if not 0 <= end_hour <= 23:
        raise ValueError(
            "end_hour must be between 0 and 23."
        )

    if start_hour > end_hour:
        raise ValueError(
            "start_hour cannot exceed end_hour."
        )

    start_datetime = datetime.combine(
        target_date,
        time(hour=start_hour),
    )

    end_datetime = datetime.combine(
        target_date,
        time(
            hour=end_hour,
            minute=59,
            second=59,
        ),
    )

    return random_datetime_between(
        start_datetime,
        end_datetime,
        rng,
    )


def format_date(value: date | None) -> str | None:
    """Format a date for CSV export."""

    if value is None:
        return None

    return value.strftime(DATE_FORMAT)


def format_datetime(
    value: datetime | None,
) -> str | None:
    """Format a timestamp for CSV export."""

    if value is None:
        return None

    return value.strftime(TIMESTAMP_FORMAT)


# =========================================================
# CONTACT AND TEXT UTILITIES
# =========================================================

def slugify(value: str) -> str:
    """Convert text into a lowercase identifier-friendly slug."""

    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", ".", normalized)
    normalized = normalized.strip(".")

    return normalized


def generate_email(
    first_name: str,
    last_name: str,
    sequence_number: int,
    domain: str = "example.com",
) -> str:
    """Generate a unique synthetic email address."""

    if sequence_number <= 0:
        raise ValueError(
            "sequence_number must be greater than zero."
        )

    local_part = slugify(
        f"{first_name}.{last_name}"
    )

    normalized_domain = domain.strip().lower()

    if not local_part:
        raise ValueError(
            "Unable to create email local part."
        )

    if "." not in normalized_domain:
        raise ValueError(
            "domain must contain a valid suffix."
        )

    return (
        f"{local_part}{sequence_number}@"
        f"{normalized_domain}"
    )


def generate_indian_phone_number(
    rng: random.Random | None = None,
) -> str:
    """Generate a synthetic 10-digit Indian mobile number."""

    random_generator = rng or random

    first_digit = random_generator.choice(
        ["6", "7", "8", "9"]
    )

    remaining_digits = "".join(
        random_generator.choices(
            string.digits,
            k=9,
        )
    )

    return first_digit + remaining_digits


def generate_pincode(
    rng: random.Random | None = None,
) -> str:
    """Generate a valid-format six-digit Indian PIN code."""

    random_generator = rng or random

    first_digit = random_generator.choice(
        "123456789"
    )

    remaining_digits = "".join(
        random_generator.choices(
            string.digits,
            k=5,
        )
    )

    return first_digit + remaining_digits


def generate_gstin(
    sequence_number: int,
    state_code: str = "27",
) -> str:
    """Generate a valid-format synthetic GSTIN-like identifier."""

    if sequence_number <= 0:
        raise ValueError(
            "sequence_number must be greater than zero."
        )

    if len(state_code) != 2 or not state_code.isdigit():
        raise ValueError(
            "state_code must contain exactly two digits."
        )

    synthetic_pan = f"RNOVA{sequence_number:04d}Z"[-10:]

    return (
        f"{state_code}"
        f"{synthetic_pan}"
        f"1Z"
        f"{sequence_number % 10}"
    )[:15]


def choose_optional_value(
    value: Any,
    null_probability: float,
    rng: random.Random | None = None,
) -> Any:
    """Return None using the configured null probability."""

    if not 0 <= null_probability <= 1:
        raise ValueError(
            "null_probability must be between 0 and 1."
        )

    random_generator = rng or random

    if random_generator.random() < null_probability:
        return None

    return value


# =========================================================
# DATAFRAME VALIDATION
# =========================================================

def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: Sequence[str],
    dataset_name: str,
) -> None:
    """Ensure required columns exist in a dataframe."""

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"{dataset_name} is missing required columns: "
            f"{missing_columns}"
        )


def validate_primary_key(
    dataframe: pd.DataFrame,
    primary_key: str,
    dataset_name: str,
) -> None:
    """Validate primary-key completeness and uniqueness."""

    validate_required_columns(
        dataframe,
        [primary_key],
        dataset_name,
    )

    if dataframe[primary_key].isna().any():
        raise ValueError(
            f"{dataset_name}.{primary_key} contains null values."
        )

    duplicates = dataframe[primary_key].duplicated().sum()

    if duplicates:
        raise ValueError(
            f"{dataset_name}.{primary_key} contains "
            f"{duplicates} duplicate values."
        )


def validate_not_null_columns(
    dataframe: pd.DataFrame,
    columns: Sequence[str],
    dataset_name: str,
) -> None:
    """Validate that mandatory columns contain no nulls."""

    validate_required_columns(
        dataframe,
        columns,
        dataset_name,
    )

    null_counts = dataframe[list(columns)].isna().sum()
    invalid = null_counts[null_counts > 0].to_dict()

    if invalid:
        raise ValueError(
            f"{dataset_name} contains nulls in mandatory "
            f"columns: {invalid}"
        )


def validate_allowed_values(
    dataframe: pd.DataFrame,
    column: str,
    allowed_values: Iterable[Any],
    dataset_name: str,
    allow_null: bool = False,
) -> None:
    """Ensure a dataframe column uses approved values."""

    validate_required_columns(
        dataframe,
        [column],
        dataset_name,
    )

    allowed_set = set(allowed_values)
    series = dataframe[column]

    if allow_null:
        series = series.dropna()

    invalid_values = set(series.unique()) - allowed_set

    if invalid_values:
        raise ValueError(
            f"{dataset_name}.{column} contains invalid values: "
            f"{sorted(invalid_values)}"
        )


def validate_foreign_key(
    child_dataframe: pd.DataFrame,
    child_column: str,
    parent_dataframe: pd.DataFrame,
    parent_column: str,
    relationship_name: str,
    allow_null: bool = False,
) -> None:
    """Validate referential integrity between two dataframes."""

    validate_required_columns(
        child_dataframe,
        [child_column],
        relationship_name,
    )

    validate_required_columns(
        parent_dataframe,
        [parent_column],
        relationship_name,
    )

    child_values = child_dataframe[child_column]

    if allow_null:
        child_values = child_values.dropna()
    elif child_values.isna().any():
        raise ValueError(
            f"{relationship_name} contains null foreign keys."
        )

    parent_values = set(
        parent_dataframe[parent_column].dropna()
    )

    missing_values = set(child_values) - parent_values

    if missing_values:
        examples = list(missing_values)[:5]

        raise ValueError(
            f"{relationship_name} contains "
            f"{len(missing_values)} invalid foreign keys. "
            f"Examples: {examples}"
        )


def validate_non_negative(
    dataframe: pd.DataFrame,
    columns: Sequence[str],
    dataset_name: str,
) -> None:
    """Validate that numeric columns contain no negative values."""

    validate_required_columns(
        dataframe,
        columns,
        dataset_name,
    )

    invalid_columns = {}

    for column in columns:
        invalid_count = (
            pd.to_numeric(
                dataframe[column],
                errors="coerce",
            )
            < 0
        ).sum()

        if invalid_count:
            invalid_columns[column] = int(invalid_count)

    if invalid_columns:
        raise ValueError(
            f"{dataset_name} contains negative values: "
            f"{invalid_columns}"
        )


# =========================================================
# CSV EXPORT
# =========================================================

def prepare_dataframe_for_csv(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Convert values into PostgreSQL-friendly CSV representations.
    """

    output = dataframe.copy()

    for column in output.columns:
        if pd.api.types.is_datetime64_any_dtype(
            output[column]
        ):
            output[column] = output[column].dt.strftime(
                TIMESTAMP_FORMAT
            )

        elif output[column].dtype == "object":
            output[column] = output[column].map(
                lambda value: (
                    format(value, "f")
                    if isinstance(value, Decimal)
                    else value
                )
            )

    return output


def export_dataframe(
    dataframe: pd.DataFrame,
    output_path: str | Path,
    expected_columns: Sequence[str] | None = None,
) -> Path:
    """Validate and export a dataframe to UTF-8 CSV."""

    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError(
            "dataframe must be a pandas DataFrame."
        )

    path = Path(output_path)
    ensure_directory(path.parent)

    if expected_columns is not None:
        validate_required_columns(
            dataframe,
            expected_columns,
            path.stem,
        )

        dataframe = dataframe[list(expected_columns)]

    prepared_dataframe = prepare_dataframe_for_csv(
        dataframe
    )

    prepared_dataframe.to_csv(
        path,
        index=False,
        encoding="utf-8",
        date_format=TIMESTAMP_FORMAT,
    )

    return path


def dataframe_summary(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> dict[str, Any]:
    """Return a compact dataset-quality summary."""

    return {
        "dataset": dataset_name,
        "rows": int(len(dataframe)),
        "columns": int(len(dataframe.columns)),
        "duplicate_rows": int(
            dataframe.duplicated().sum()
        ),
        "total_null_values": int(
            dataframe.isna().sum().sum()
        ),
        "memory_mb": round(
            dataframe.memory_usage(
                deep=True
            ).sum()
            / 1_048_576,
            4,
        ),
    }


if __name__ == "__main__":
    test_rng = set_random_seeds(42)

    print("RetailNova utilities loaded.")
    print("Sample UUID:", generate_uuid(test_rng))
    print(
        "Sample code:",
        generate_sequential_code("CUS", 1),
    )
    print(
        "Sample phone:",
        generate_indian_phone_number(test_rng),
    )
