# BrisHandicapper/src/config/paths.py

from pathlib import Path

# This file centralizes all main directory and file paths for the project.
# By defining them here, we avoid hardcoding paths in multiple scripts,
# making the project more maintainable and less prone to errors.

# The root directory of the project (BrisHandicapper)
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Key data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Reports directory
REPORTS_DIR = PROJECT_ROOT / "reports"
