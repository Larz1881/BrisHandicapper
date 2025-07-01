#!/usr/bin/env python
"""
Main analysis orchestrator for the BrisHandicapper project.

This script loads the processed race and past performance data, then executes
the sequential steps of the "Adapted Handicapping Process" for each race.
"""
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

import pandas as pd

# --- Module Imports ---
try:
    from config import settings, paths
    from bris_handicapper.analysis.contender_filter import isolate_contenders
    from bris_handicapper.analysis.grouper import group_contenders
    from bris_handicapper.analysis.situational_analyzer import adjust_groups_for_situation
    from bris_handicapper.reporting.reporter import generate_llm_report_data, save_report
except ImportError as e:
    print(f"FATAL: Could not import necessary modules. Error: {e}")
    print("\nPlease ensure you have:")
    print("1. Run 'pip install -e .' from the project root directory")
    print("2. Created all necessary __init__.py files")
    print("3. Are running this from the correct environment")
    sys.exit(1)

# --- Basic Logging Setup for Standalone Execution ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

def handicap_races():
    """
    Main function to run the handicapping process on all races for the day.
    """
    logger.info("Loading processed data for handicapping...")

    try:
        current_races_df = pd.read_parquet(settings.CURRENT_RACE_INFO_FILE)
        past_starts_df = pd.read_parquet(settings.PAST_STARTS_LONG_FILE)
        logger.info("Successfully loaded current race info and past starts data.")
    except FileNotFoundError as e:
        logger.error(f"FATAL: Could not load processed data file. Please run the data pipeline first. Error: {e}")
        return

    races_to_handicap = current_races_df[['track', 'race']].drop_duplicates().to_dict('records')

    for race_info in races_to_handicap:
        track_code = race_info['track']
        race_num = race_info['race']

        logger.info(f"\n{'='*60}\nProcessing: {track_code} - Race {race_num}\n{'='*60}")

        single_race_df = current_races_df[
            (current_races_df['track'] == track_code) &
            (current_races_df['race'] == race_num)
        ]

        # --- Execute the 6-Step Handicapping Process ---
        # Step 2: Isolate Contenders
        contenders = isolate_contenders(single_race_df, past_starts_df)
        if contenders.empty:
            logger.warning(f"No contenders identified for Race {race_num}, skipping.")
            continue

        # Step 3: Group Contenders
        initial_groups = group_contenders(contenders, past_starts_df)

        # Steps 4 & 5: Adjust Groups
        final_groups, adjustments = adjust_groups_for_situation(initial_groups, contenders, past_starts_df)

        # Step 6: Generate and Save Report
        report_data = generate_llm_report_data(final_groups, contenders, past_starts_df, adjustments)
        save_report(report_data, paths.REPORTS_DIR)

        logger.info(f"Finished processing {track_code} - Race {race_num}. Report saved.")

if __name__ == "__main__":
    logger.info("Executing handicap.py as a standalone script.")
    handicap_races()
