# BrisHandicapper/src/config/settings.py

from .paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, PROJECT_ROOT

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

# --- Cache Directory and Files ---
# Directory for cached files like specification and dictionary data
CACHE_DIR = PROJECT_ROOT / "cache"

# Brisnet specification cache and dictionary paths
BRIS_SPEC_CACHE = CACHE_DIR / "bris_spec.pkl"
BRIS_DICT = CACHE_DIR / "bris_dict.txt"

# --- Primary Processed Data File ---
PARSED_RACE_DATA_FILE = PROCESSED_DATA_DIR / "parsed_race_data_full.parquet"

# Aliases expected by data-processing modules
PARSED_RACE_DATA = PARSED_RACE_DATA_FILE
CURRENT_RACE_INFO = CURRENT_RACE_INFO_FILE
PAST_STARTS_LONG = PAST_STARTS_LONG_FILE
WORKOUTS_LONG = WORKOUTS_LONG_FILE


# You can add other settings here as the project grows, such as model parameters,
# feature lists, or API keys.
