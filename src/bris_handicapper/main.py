#!/usr/bin/env python
"""
Main pipeline orchestrator for the BrisHandicapper project.

This script discovers the latest Brisnet data file and executes the core data
processing sequence to parse, clean, and transform the data into usable formats.
"""
import sys
import logging
from pathlib import Path
from datetime import datetime

# --- Module Imports ---
# When installed as a package, these imports work correctly
try:
    from config.config import settings
    from bris_handicapper.data_processing.bris_spec_new import main as parse_bris_data
    from bris_handicapper.data_processing.current_race_info import main as create_current_info
    from bris_handicapper.data_processing.transform_workouts import main as transform_workouts_data
    from bris_handicapper.data_processing.transform_past_starts import main as transform_past_starts_data
except ImportError as e:
    print(f"FATAL: Could not import necessary modules. Error: {e}")
    print("\nPlease ensure you have:")
    print("1. Run 'pip install -e .' from the project root directory")
    print("2. Created all necessary __init__.py files")
    print("3. Are running this from the correct environment")
    sys.exit(1)

# --- Logging Setup ---
# Get project root from the installed package location
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE_PATH = LOG_DIR / f'pipeline_{datetime.now():%Y%m%d_%H%M%S}.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def find_latest_drf_file() -> Path:
    """Finds the most recent DRF file in the raw data directory.""" 
    logger.info(f"Searching for DRF files in: {settings.RAW_DATA_DIR} using pattern: '{settings.DRF_PATTERN}'")

    if not settings.RAW_DATA_DIR.exists():
        msg = f"Raw data directory does not exist: {settings.RAW_DATA_DIR}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    drf_files = list(settings.RAW_DATA_DIR.glob(settings.DRF_PATTERN))

    if not drf_files:
        msg = f"No DRF files found matching pattern '{settings.DRF_PATTERN}' in {settings.RAW_DATA_DIR}"
        logger.error(msg)
        raise FileNotFoundError(msg)

    # Find the file with the most recent modification time
    latest_file = max(drf_files, key=lambda p: p.stat().st_mtime)
    logger.info(f"Found latest DRF file: {latest_file.name}")
    return latest_file

def run():
    """
    Executes the complete data processing pipeline in sequence.
    """
    logger.info("==============================================")
    logger.info("=== Starting Brisnet Data Processing Pipeline ===")
    logger.info("==============================================")

    try:
        # Step 0: Find the latest data file to process
        drf_to_process = find_latest_drf_file()

        # Execute the pipeline steps
        logger.info("Step 1: Parsing Brisnet data...")
        parse_bris_data(drf_file_path_arg=drf_to_process)

        logger.info("Step 2: Creating current race info...")
        create_current_info()

        logger.info("Step 3: Transforming workouts...")
        transform_workouts_data()

        logger.info("Step 4: Transforming past starts...")
        transform_past_starts_data()

        logger.info("=============================================")
        logger.info("=== Pipeline Finished Successfully      ===")
        logger.info("=============================================")

    except FileNotFoundError as e:
        logger.error(f"PIPELINE HALTED: A required file was not found. Details: {e}", exc_info=False)
    except Exception as e:
        logger.error(f"PIPELINE FAILED with an unexpected error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run()
