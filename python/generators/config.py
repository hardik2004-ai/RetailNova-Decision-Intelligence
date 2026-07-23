"""
RetailNova Decision Intelligence Platform
Synthetic Data Engine Configuration

This module contains the central configuration used by all
RetailNova synthetic-data generators.

Author: Hardik Narigra
"""

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Dict


# =========================================================
# PROJECT PATHS
# =========================================================

# In Google Colab, generated files will be stored here.
COLAB_PROJECT_ROOT = Path("/content/retailnova")

MASTER_DATA_DIR = COLAB_PROJECT_ROOT / "master_data"
GENERATED_DATA_DIR = COLAB_PROJECT_ROOT / "generated_data"
LOG_DIR = COLAB_PROJECT_ROOT / "logs"


# =========================================================
# DATASET SCALE
# =========================================================

DEVELOPMENT_SCALE: Dict[str, int] = {
    "categories": 15,
    "brands": 37,
    "suppliers": 20,
    "locations": 20,
    "products": 50,
    "customers": 100,
    "addresses": 140,
    "memberships": 25,
    "inventory_records": 400,
    "orders": 200,
    "order_items": 600,
    "payments": 200,
    "returns": 25,
    "purchase_orders": 30,
    "purchase_order_items": 120,
}


FULL_SCALE: Dict[str, int] = {
    "categories": 15,
    "brands": 37,
    "suppliers": 20,
    "locations": 20,
    "products": 5_000,
    "customers": 50_000,
    "addresses": 70_000,
    "memberships": 10_000,
    "inventory_records": 40_000,
    "orders": 500_000,
    "order_items": 1_500_000,
    "payments": 500_000,
    "returns": 60_000,
    "purchase_orders": 8_000,
    "purchase_order_items": 40_000,
}


# =========================================================
# MAIN CONFIGURATION
# =========================================================

@dataclass(frozen=True)
class GeneratorConfig:
    """
    Immutable configuration for the RetailNova synthetic-data engine.
    """

    environment: str
    random_seed: int
    simulation_start_date: date
    simulation_end_date: date
    output_directory: Path
    master_data_directory: Path
    log_directory: Path
    chunk_size: int
    dataset_scale: Dict[str, int]

    def get_record_count(self, dataset_name: str) -> int:
        """
        Return the configured record count for a dataset.

        Parameters
        ----------
        dataset_name:
            Name of the dataset, such as 'customers' or 'orders'.

        Returns
        -------
        int
            Number of records configured for the dataset.

        Raises
        ------
        KeyError
            If the requested dataset is not configured.
        """

        if dataset_name not in self.dataset_scale:
            available = ", ".join(sorted(self.dataset_scale.keys()))

            raise KeyError(
                f"Unknown dataset '{dataset_name}'. "
                f"Available datasets: {available}"
            )

        return self.dataset_scale[dataset_name]

    def create_directories(self) -> None:
        """
        Create all directories required by the generation pipeline.
        """

        directories = [
            self.output_directory,
            self.master_data_directory,
            self.log_directory,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def validate(self) -> None:
        """
        Validate the configuration before data generation begins.
        """

        supported_environments = {"development", "full"}

        if self.environment not in supported_environments:
            raise ValueError(
                f"Unsupported environment '{self.environment}'. "
                f"Expected one of: {sorted(supported_environments)}"
            )

        if self.random_seed < 0:
            raise ValueError("random_seed must be zero or a positive integer.")

        if self.simulation_start_date > self.simulation_end_date:
            raise ValueError(
                "simulation_start_date cannot be later than "
                "simulation_end_date."
            )

        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        for dataset_name, record_count in self.dataset_scale.items():
            if not isinstance(record_count, int):
                raise TypeError(
                    f"Record count for '{dataset_name}' must be an integer."
                )

            if record_count < 0:
                raise ValueError(
                    f"Record count for '{dataset_name}' cannot be negative."
                )


# =========================================================
# CONFIGURATION FACTORY
# =========================================================

def get_config(environment: str = "development") -> GeneratorConfig:
    """
    Create and return a validated RetailNova generator configuration.

    Parameters
    ----------
    environment:
        Use 'development' for small test datasets.
        Use 'full' for the complete enterprise dataset.

    Returns
    -------
    GeneratorConfig
        Validated generator configuration.
    """

    normalized_environment = environment.strip().lower()

    if normalized_environment == "development":
        dataset_scale = DEVELOPMENT_SCALE.copy()
        chunk_size = 10_000

    elif normalized_environment == "full":
        dataset_scale = FULL_SCALE.copy()
        chunk_size = 100_000

    else:
        raise ValueError(
            "environment must be either 'development' or 'full'."
        )

    config = GeneratorConfig(
        environment=normalized_environment,
        random_seed=42,
        simulation_start_date=date(2023, 1, 1),
        simulation_end_date=date(2025, 12, 31),
        output_directory=GENERATED_DATA_DIR,
        master_data_directory=MASTER_DATA_DIR,
        log_directory=LOG_DIR,
        chunk_size=chunk_size,
        dataset_scale=dataset_scale,
    )

    config.validate()
    config.create_directories()

    return config


# Default configuration used by generator modules.
CONFIG = get_config("development")


# =========================================================
# DIRECT EXECUTION
# =========================================================

if __name__ == "__main__":
    print("RetailNova configuration loaded successfully.")
    print(f"Environment: {CONFIG.environment}")
    print(f"Random seed: {CONFIG.random_seed}")

    print(
        "Simulation period: "
        f"{CONFIG.simulation_start_date} to "
        f"{CONFIG.simulation_end_date}"
    )

    print(f"Output directory: {CONFIG.output_directory}")
    print(f"Configured datasets: {len(CONFIG.dataset_scale)}")
    print(f"Development orders: {CONFIG.get_record_count('orders')}")
