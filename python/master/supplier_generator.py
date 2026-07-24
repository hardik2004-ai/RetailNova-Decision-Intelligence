

"""
RetailNova Decision Intelligence Platform
Supplier Master Data Generator

Generates the supplier.csv dataset for the PostgreSQL
supplier table.

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
    )
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
        "before importing supplier_generator."
    ) from error


# =========================================================
# SUPPLIER MASTER DATA
# =========================================================

SUPPLIER_RECORDS = (
    (
        "NovaTech Distribution Private Limited",
        "Arjun Mehta",
        "arjun.mehta@novatech.example.com",
        "9876500001",
        "Andheri East Industrial Estate",
        "Mumbai",
        "Maharashtra",
        "400093",
    ),
    (
        "Western Digital Commerce Limited",
        "Sneha Kulkarni",
        "sneha.kulkarni@westerndigitalcommerce.example.com",
        "9876500002",
        "Hinjewadi Commercial Park",
        "Pune",
        "Maharashtra",
        "411057",
    ),
    (
        "Metro Consumer Goods Private Limited",
        "Rohan Patil",
        "rohan.patil@metroconsumer.example.com",
        "9876500003",
        "Wagle Industrial Estate",
        "Thane",
        "Maharashtra",
        "400604",
    ),
    (
        "NorthStar Retail Supplies Limited",
        "Priya Deshmukh",
        "priya.deshmukh@northstarretail.example.com",
        "9876500004",
        "Satpur Industrial Area",
        "Nashik",
        "Maharashtra",
        "422007",
    ),
    (
        "Central India Wholesale Corporation",
        "Aditya Joshi",
        "aditya.joshi@centralindiawholesale.example.com",
        "9876500005",
        "Hingna Industrial Area",
        "Nagpur",
        "Maharashtra",
        "440016",
    ),
    (
        "Aarav Electronics Distribution Limited",
        "Neha Shah",
        "neha.shah@aaravelectronics.example.com",
        "9876500006",
        "Naroda Industrial Estate",
        "Ahmedabad",
        "Gujarat",
        "382330",
    ),
    (
        "BlueRiver Fashion Supply Private Limited",
        "Kunal Patel",
        "kunal.patel@blueriverfashion.example.com",
        "9876500007",
        "Udhna Commercial Zone",
        "Surat",
        "Gujarat",
        "394210",
    ),
    (
        "Prime Household Products Limited",
        "Meera Trivedi",
        "meera.trivedi@primehousehold.example.com",
        "9876500008",
        "Makarpura Industrial Estate",
        "Vadodara",
        "Gujarat",
        "390010",
    ),
    (
        "Southern Technology Partners Limited",
        "Vikram Rao",
        "vikram.rao@southerntechnology.example.com",
        "9876500009",
        "Whitefield Technology Park",
        "Bengaluru",
        "Karnataka",
        "560066",
    ),
    (
        "Heritage Furniture Suppliers Private Limited",
        "Ananya Shetty",
        "ananya.shetty@heritagefurniture.example.com",
        "9876500010",
        "Hebbal Industrial Area",
        "Mysuru",
        "Karnataka",
        "570016",
    ),
    (
        "Coastal Appliance Distributors Limited",
        "Karthik Iyer",
        "karthik.iyer@coastalappliance.example.com",
        "9876500011",
        "Guindy Industrial Estate",
        "Chennai",
        "Tamil Nadu",
        "600032",
    ),
    (
        "GreenLeaf Personal Care Suppliers",
        "Divya Natarajan",
        "divya.natarajan@greenleafcare.example.com",
        "9876500012",
        "SIDCO Industrial Estate",
        "Coimbatore",
        "Tamil Nadu",
        "641021",
    ),
    (
        "Deccan Sports and Fitness Supply Limited",
        "Rahul Reddy",
        "rahul.reddy@deccansports.example.com",
        "9876500013",
        "Balanagar Industrial Area",
        "Hyderabad",
        "Telangana",
        "500037",
    ),
    (
        "Capital Office Solutions Private Limited",
        "Ishita Sharma",
        "ishita.sharma@capitaloffice.example.com",
        "9876500014",
        "Okhla Industrial Estate",
        "New Delhi",
        "Delhi",
        "110020",
    ),
    (
        "Eastern Books and Media Distributors",
        "Sourav Banerjee",
        "sourav.banerjee@easternbooks.example.com",
        "9876500015",
        "Salt Lake Sector V",
        "Kolkata",
        "West Bengal",
        "700091",
    ),
    (
        "Royal Home and Kitchen Suppliers Limited",
        "Nidhi Rathore",
        "nidhi.rathore@royalhomekitchen.example.com",
        "9876500016",
        "Vishwakarma Industrial Area",
        "Jaipur",
        "Rajasthan",
        "302013",
    ),
    (
        "Ganga Grocery Distribution Private Limited",
        "Abhishek Verma",
        "abhishek.verma@gangagrocery.example.com",
        "9876500017",
        "Amausi Industrial Area",
        "Lucknow",
        "Uttar Pradesh",
        "226008",
    ),
    (
        "Malwa Automotive Supplies Limited",
        "Pooja Chouhan",
        "pooja.chouhan@malwaautomotive.example.com",
        "9876500018",
        "Sanwer Road Industrial Area",
        "Indore",
        "Madhya Pradesh",
        "452015",
    ),
    (
        "LakeCity Toys and Games Distributors",
        "Nitin Tiwari",
        "nitin.tiwari@lakecitytoys.example.com",
        "9876500019",
        "Govindpura Industrial Area",
        "Bhopal",
        "Madhya Pradesh",
        "462023",
    ),
    (
        "NCR Smart Home Distribution Limited",
        "Sakshi Gupta",
        "sakshi.gupta@ncrsmarthome.example.com",
        "9876500020",
        "Sector 63 Industrial Park",
        "Noida",
        "Uttar Pradesh",
        "201301",
    ),
)


SUPPLIER_COLUMNS = [
    "supplier_id",
    "supplier_name",
    "contact_person",
    "email",
    "phone_number",
    "address",
    "city",
    "state",
    "country",
    "postal_code",
    "is_active",
    "created_at",
    "updated_at",
]


MASTER_DATA_CREATED_AT = "2023-01-01 00:00:00+00:00"


# =========================================================
# GENERATOR
# =========================================================

def generate_suppliers(
    config: GeneratorConfig = CONFIG,
) -> pd.DataFrame:
    """Generate the RetailNova supplier master dataset."""

    expected_count = config.get_record_count("suppliers")
    available_count = len(SUPPLIER_RECORDS)

    if expected_count != available_count:
        raise ValueError(
            "Supplier configuration mismatch: "
            f"configured={expected_count}, "
            f"available={available_count}."
        )

    records = []

    for supplier_id, supplier_data in enumerate(
        SUPPLIER_RECORDS,
        start=1,
    ):
        (
            supplier_name,
            contact_person,
            email,
            phone_number,
            address,
            city,
            state,
            postal_code,
        ) = supplier_data

        records.append(
            {
                "supplier_id": supplier_id,
                "supplier_name": supplier_name,
                "contact_person": contact_person,
                "email": email,
                "phone_number": phone_number,
                "address": address,
                "city": city,
                "state": state,
                "country": COMPANY_COUNTRY,
                "postal_code": postal_code,
                "is_active": True,
                "created_at": MASTER_DATA_CREATED_AT,
                "updated_at": MASTER_DATA_CREATED_AT,
            }
        )

    supplier_dataframe = pd.DataFrame(
        records,
        columns=SUPPLIER_COLUMNS,
    )

    validate_suppliers(supplier_dataframe, config)

    return supplier_dataframe


# =========================================================
# VALIDATION
# =========================================================

def validate_suppliers(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> None:
    """Validate supplier data before CSV export."""

    expected_count = config.get_record_count("suppliers")

    if len(dataframe) != expected_count:
        raise ValueError(
            f"Expected {expected_count} suppliers, "
            f"found {len(dataframe)}."
        )

    if list(dataframe.columns) != SUPPLIER_COLUMNS:
        raise ValueError(
            "Supplier column order does not match the "
            "PostgreSQL supplier table."
        )

    validate_primary_key(
        dataframe,
        "supplier_id",
        "supplier",
    )

    validate_not_null_columns(
        dataframe,
        SUPPLIER_COLUMNS,
        "supplier",
    )

    unique_columns = [
        "supplier_name",
        "email",
        "phone_number",
    ]

    for column in unique_columns:
        if dataframe[column].duplicated().any():
            duplicates = (
                dataframe.loc[
                    dataframe[column].duplicated(keep=False),
                    column,
                ]
                .unique()
                .tolist()
            )

            raise ValueError(
                f"supplier.{column} must be unique. "
                f"Duplicates: {duplicates}"
            )

    length_limits = {
        "supplier_name": 150,
        "contact_person": 150,
        "email": 255,
        "phone_number": 20,
        "address": 255,
        "city": 100,
        "state": 100,
        "country": 100,
        "postal_code": 20,
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
                f"supplier.{column} exceeds "
                f"VARCHAR({maximum_length})."
            )

    email_pattern = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    invalid_emails = dataframe.loc[
        ~dataframe["email"].str.match(email_pattern),
        "email",
    ].tolist()

    if invalid_emails:
        raise ValueError(
            f"Invalid supplier email addresses: {invalid_emails}"
        )

    invalid_phones = dataframe.loc[
        ~dataframe["phone_number"].str.match(r"^[6-9]\d{9}$"),
        "phone_number",
    ].tolist()

    if invalid_phones:
        raise ValueError(
            f"Invalid Indian phone numbers: {invalid_phones}"
        )

    invalid_postal_codes = dataframe.loc[
        ~dataframe["postal_code"].str.match(r"^[1-9]\d{5}$"),
        "postal_code",
    ].tolist()

    if invalid_postal_codes:
        raise ValueError(
            f"Invalid Indian postal codes: {invalid_postal_codes}"
        )

    invalid_cities = (
        set(dataframe["city"])
        - set(INDIAN_CITIES)
    )

    if invalid_cities:
        raise ValueError(
            f"Unsupported supplier cities: {invalid_cities}"
        )

    invalid_states = (
        set(dataframe["state"])
        - set(INDIAN_STATES)
    )

    if invalid_states:
        raise ValueError(
            f"Unsupported supplier states: {invalid_states}"
        )

    if not dataframe["country"].eq(
        COMPANY_COUNTRY
    ).all():
        raise ValueError(
            f"All suppliers must use country={COMPANY_COUNTRY}."
        )

    if not dataframe["is_active"].map(
        lambda value: isinstance(value, bool)
    ).all():
        raise ValueError(
            "supplier.is_active must contain Boolean values."
        )

    if not dataframe["is_active"].all():
        raise ValueError(
            "All initial supplier records must be active."
        )


# =========================================================
# CSV EXPORT
# =========================================================

def export_suppliers(
    dataframe: pd.DataFrame,
    config: GeneratorConfig = CONFIG,
) -> Path:
    """Validate and export supplier.csv."""

    validate_suppliers(dataframe, config)

    output_path = (
        config.output_directory
        / CSV_FILE_NAMES["supplier"]
    )

    return export_dataframe(
        dataframe,
        output_path,
        expected_columns=SUPPLIER_COLUMNS,
    )


def generate_and_export_suppliers(
    config: GeneratorConfig = CONFIG,
) -> tuple[pd.DataFrame, Path]:
    """Generate, validate and export supplier data."""

    dataframe = generate_suppliers(config)
    output_path = export_suppliers(dataframe, config)

    return dataframe, output_path


if __name__ == "__main__":
    supplier_df, csv_path = (
        generate_and_export_suppliers()
    )

    print("Supplier generation completed.")
    print(dataframe_summary(supplier_df, "supplier"))
    print(f"CSV: {csv_path}")
