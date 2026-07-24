
"""
RetailNova Decision Intelligence Platform
Membership Data Generator

Generates NovaPremium membership records for existing
RetailNova customers.

Author: Hardik Narigra
"""

from datetime import date, timedelta
from pathlib import Path

import pandas as pd

try:
    from config import CONFIG, GeneratorConfig
    from constants import (
        CSV_FILE_NAMES,
        MEMBERSHIP_BILLING_CYCLES,
        MEMBERSHIP_STATUSES,
        MONTHLY_MEMBERSHIP_DURATION_DAYS,
        YEARLY_MEMBERSHIP_DURATION_DAYS,
    )
    from probability_models import (
        MEMBERSHIP_BILLING_CYCLE_WEIGHTS,
        MEMBERSHIP_STATUS_WEIGHTS,
    )
    from utils import (
        dataframe_summary,
        export_dataframe,
        generate_sequential_code,
        random_date_between,
        set_random_seeds,
        validate_allowed_values,
        validate_foreign_key,
        validate_not_null_columns,
        validate_primary_key,
        validate_required_columns,
    )
except ImportError as error:
    raise ImportError(
        "Unable to import RetailNova generator modules. "
        "Add /content/retailnova/python/generators to sys.path "
        "before importing membership_generator."
    ) from error


MEMBERSHIP_COLUMNS = [
    "membership_id",
    "customer_id",
    "membership_number",
    "status",
    "start_date",
    "end_date",
    "created_at",
    "updated_at",
]


def load_customer_data(
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Load customer.csv for membership generation."""

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
        parse_dates=["registration_date"],
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


def choose_membership_status(
    rng,
) -> str:
    """Choose membership status using configured weights."""

    statuses = list(
        MEMBERSHIP_STATUS_WEIGHTS.keys()
    )

    weights = list(
        MEMBERSHIP_STATUS_WEIGHTS.values()
    )

    return rng.choices(
        statuses,
        weights=weights,
        k=1,
    )[0]


def choose_billing_cycle(
    rng,
) -> str:
    """Choose monthly or yearly billing."""

    cycles = list(
        MEMBERSHIP_BILLING_CYCLE_WEIGHTS.keys()
    )

    weights = list(
        MEMBERSHIP_BILLING_CYCLE_WEIGHTS.values()
    )

    return rng.choices(
        cycles,
        weights=weights,
        k=1,
    )[0]


def get_membership_duration(
    billing_cycle: str,
) -> int:
    """Return membership duration in days."""

    if billing_cycle == "MONTHLY":
        return MONTHLY_MEMBERSHIP_DURATION_DAYS

    if billing_cycle == "YEARLY":
        return YEARLY_MEMBERSHIP_DURATION_DAYS

    raise ValueError(
        f"Unsupported billing cycle: {billing_cycle}"
    )


def create_membership_dates(
    registration_date: date,
    status: str,
    billing_cycle: str,
    simulation_end_date: date,
    rng,
) -> tuple[date, date | None]:
    """Create logically consistent membership dates."""

    duration_days = get_membership_duration(
        billing_cycle
    )

    if status == "ACTIVE":
        start_date = random_date_between(
            registration_date,
            simulation_end_date,
            rng,
        )

        # Null end date represents an ongoing membership.
        return start_date, None

    if status == "EXPIRED":
        latest_start_date = (
            simulation_end_date
            - timedelta(days=duration_days)
        )

        # A recently registered customer may not have enough
        # history for a yearly expired membership.
        if latest_start_date < registration_date:
            duration_days = (
                MONTHLY_MEMBERSHIP_DURATION_DAYS
            )

            latest_start_date = (
                simulation_end_date
                - timedelta(days=duration_days)
            )

        if latest_start_date < registration_date:
            raise ValueError(
                "Customer registration date does not allow "
                "an expired membership."
            )

        start_date = random_date_between(
            registration_date,
            latest_start_date,
            rng,
        )

        end_date = start_date + timedelta(
            days=duration_days
        )

        return start_date, end_date

    if status == "CANCELLED":
        start_date = random_date_between(
            registration_date,
            simulation_end_date,
            rng,
        )

        natural_end_date = start_date + timedelta(
            days=duration_days
        )

        latest_cancellation_date = min(
            natural_end_date,
            simulation_end_date,
        )

        end_date = random_date_between(
            start_date,
            latest_cancellation_date,
            rng,
        )

        return start_date, end_date

    raise ValueError(
        f"Unsupported membership status: {status}"
    )


def generate_memberships(
    customer_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Generate NovaPremium memberships."""

    membership_count = config.get_record_count(
        "memberships"
    )

    customer_ids = (
        customer_dataframe["customer_id"]
        .astype(int)
        .tolist()
    )

    if membership_count > len(customer_ids):
        raise ValueError(
            "Membership count cannot exceed customer count "
            "when one membership per customer is allowed."
        )

    rng = set_random_seeds(config.random_seed + 2)

    selected_customer_ids = rng.sample(
        customer_ids,
        membership_count,
    )

    registration_lookup = {
        int(row.customer_id): (
            pd.Timestamp(
                row.registration_date
            ).date()
        )
        for row in customer_dataframe.itertuples()
    }

    records = []

    for membership_id, customer_id in enumerate(
        selected_customer_ids,
        start=1,
    ):
        status = choose_membership_status(rng)
        billing_cycle = choose_billing_cycle(rng)

        registration_date = registration_lookup[
            customer_id
        ]

        try:
            start_date, end_date = (
                create_membership_dates(
                    registration_date,
                    status,
                    billing_cycle,
                    config.simulation_end_date,
                    rng,
                )
            )

        except ValueError:
            # Very recent registrations cannot have expired
            # memberships, so keep them active.
            status = "ACTIVE"

            start_date, end_date = (
                create_membership_dates(
                    registration_date,
                    status,
                    billing_cycle,
                    config.simulation_end_date,
                    rng,
                )
            )

        timestamp = (
            f"{start_date} 00:00:00+00:00"
        )

        records.append(
            {
                "membership_id": membership_id,
                "customer_id": customer_id,
                "membership_number": (
                    generate_sequential_code(
                        "MEM",
                        membership_id,
                    )
                ),
                "status": status,
                "start_date": start_date,
                "end_date": end_date,
                "created_at": timestamp,
                "updated_at": timestamp,
            }
        )

    membership_dataframe = pd.DataFrame(
        records,
        columns=MEMBERSHIP_COLUMNS,
    )

    validate_memberships(
        membership_dataframe,
        customer_dataframe,
        config,
    )

    return membership_dataframe


def validate_memberships(
    dataframe: pd.DataFrame,
    customer_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate memberships before export."""

    expected_count = config.get_record_count(
        "memberships"
    )

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} memberships, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != MEMBERSHIP_COLUMNS:
        raise ValueError(
            "Membership column order does not match the "
            "PostgreSQL membership table."
        )

    validate_primary_key(
        dataframe,
        "membership_id",
        "membership",
    )

    validate_not_null_columns(
        dataframe,
        [
            "membership_id",
            "customer_id",
            "membership_number",
            "status",
            "start_date",
            "created_at",
            "updated_at",
        ],
        "membership",
    )

    validate_foreign_key(
        dataframe,
        "customer_id",
        customer_dataframe,
        "customer_id",
        "membership.customer_id -> customer.customer_id",
    )

    validate_allowed_values(
        dataframe,
        "status",
        MEMBERSHIP_STATUSES,
        "membership",
    )

    if dataframe["customer_id"].duplicated().any():
        raise ValueError(
            "A customer cannot have multiple membership "
            "records in the current model."
        )

    if dataframe[
        "membership_number"
    ].duplicated().any():
        raise ValueError(
            "membership_number must be unique."
        )

    if (
        dataframe["membership_number"]
        .str.len()
        .gt(30)
        .any()
    ):
        raise ValueError(
            "membership_number exceeds VARCHAR(30)."
        )

    start_dates = pd.to_datetime(
        dataframe["start_date"]
    )

    end_dates = pd.to_datetime(
        dataframe["end_date"]
    )

    invalid_date_order = (
        end_dates.notna()
        & (end_dates < start_dates)
    )

    if invalid_date_order.any():
        raise ValueError(
            "membership.end_date cannot precede "
            "membership.start_date."
        )

    active_with_end_date = (
        dataframe["status"].eq("ACTIVE")
        & dataframe["end_date"].notna()
    )

    if active_with_end_date.any():
        raise ValueError(
            "Active memberships must have a null end_date "
            "in the current model."
        )

    inactive_without_end_date = (
        dataframe["status"].isin(
            ["EXPIRED", "CANCELLED"]
        )
        & dataframe["end_date"].isna()
    )

    if inactive_without_end_date.any():
        raise ValueError(
            "Expired and cancelled memberships require "
            "an end_date."
        )


def export_memberships(
    dataframe: pd.DataFrame,
    customer_dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export membership.csv."""

    validate_memberships(
        dataframe,
        customer_dataframe,
        config,
    )

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["membership"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=MEMBERSHIP_COLUMNS,
    )


def generate_and_export_memberships(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Generate and export memberships."""

    customer_dataframe = load_customer_data(config)

    membership_dataframe = generate_memberships(
        customer_dataframe,
        config,
    )

    output_path = export_memberships(
        membership_dataframe,
        customer_dataframe,
        config,
    )

    return membership_dataframe, output_path


if __name__ == "__main__":
    membership_df, csv_path = (
        generate_and_export_memberships()
    )

    print("Membership generation completed.")
    print(
        dataframe_summary(
            membership_df,
            "membership",
        )
    )
    print(f"CSV: {csv_path}")
