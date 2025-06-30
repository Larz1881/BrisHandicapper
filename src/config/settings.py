# BrisHandicapper/src/config/settings.py

from .paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

# This file contains configuration settings used across the application,
# particularly by the main pipeline script.

# --- File Patterns ---
# The glob pattern to find Brisnet DRF files.
# The '[dD][rR][fF]' part makes the extension matching case-insensitive.
DRF_PATTERN = "*.[dD][rR][fF]"

# --- Input/Output Directories ---
# These are imported from the central paths configuration for consistency.
RAW_DATA_DIR = RAW_DATA_DIR
PROCESSED_DATA_DIR = PROCESSED_DATA_DIR

# --- Processed File Names ---
# Centralizing the names of the key processed files.
CURRENT_RACE_INFO_FILE = PROCESSED_DATA_DIR / "current_race_info.parquet"
PAST_STARTS_LONG_FILE = PROCESSED_DATA_DIR / "past_starts_long_format.parquet"
WORKOUTS_LONG_FILE = PROCESSED_DATA_DIR / "workouts_long_format.parquet"


# You can add other settings here as the project grows, such as model parameters,
# feature lists, or API keys.
