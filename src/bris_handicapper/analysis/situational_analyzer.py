#!/usr/bin/env python
"""
Situational analysis module for the BrisHandicapper project.

This script implements Steps 4 & 5 of the Adapted Handicapping Process. It takes
the initial contender groups and adjusts them based on pace scenarios, pedigree
suitability for the race conditions, and key form factors like trainer and
jockey statistics.
"""
import logging
import pandas as pd
from typing import Dict, List, Any, Set, Tuple

logger = logging.getLogger(__name__)

# --- Constants for Situational Analysis ---
EARLY_RUN_STYLES = ['E', 'E/P']
PRESSING_RUN_STYLES = ['P', 'S']
TURF_SURFACE = 'T'
WET_SURFACES = ['M', 'S']
WET_TRACK_CONDITIONS = ['M', 'S', 'SY']
PEDIGREE_IMPROVEMENT_THRESHOLD = 10
TJ_COMBO_ROI_THRESHOLD = 2.0
TJ_COMBO_MIN_STARTS = 10

def analyze_pace_scenario(contenders_df: pd.DataFrame) -> str:
    """
    Analyzes the running styles of contenders to predict the race's pace shape.
    """
    early_runners = contenders_df[contenders_df['bris_run_style_designation'].isin(EARLY_RUN_STYLES)]
    if len(early_runners) == 1:
        logger.info("Pace Scenario: Lone Speed detected.")
        return 'Lone Speed'
    elif len(early_runners) > 1:
        if 'E' in early_runners['bris_run_style_designation'].values:
            e_horses = early_runners[early_runners['bris_run_style_designation'] == 'E']
            if len(e_horses) == 1:
                logger.info("Pace Scenario: Likely Lone Speed (one dominant 'E' horse).")
                return 'Lone Speed'
        logger.info("Pace Scenario: Pace Duel is likely.")
        return 'Pace Duel'
    else:
        logger.info("Pace Scenario: Unclear (no dominant front-runners).")
        return 'Unclear'

def get_situational_adjustments(contenders_df: pd.DataFrame, past_starts_df: pd.DataFrame, pace_scenario: str) -> Dict[str, Dict[Any, str]]:
    """
    Determines which horses should be upgraded or downgraded and why.
    """
    adjustments = {'upgrade': {}, 'downgrade': {}}
    for _, horse in contenders_df.iterrows():
        prog_num = horse['program_number_if_available']
        run_style = horse['bris_run_style_designation']
        if pace_scenario == 'Lone Speed' and run_style in EARLY_RUN_STYLES:
            adjustments['upgrade'][prog_num] = "Advantaged by Lone Speed scenario"
        elif pace_scenario == 'Pace Duel' and run_style in PRESSING_RUN_STYLES:
            adjustments['upgrade'][prog_num] = "Advantaged by Pace Duel scenario"
        elif pace_scenario == 'Pace Duel' and run_style in EARLY_RUN_STYLES:
            adjustments['downgrade'][prog_num] = "Disadvantaged by Pace Duel scenario"

        horse_pps = past_starts_df[past_starts_df['program_number_if_available'] == prog_num]
        if horse['surface'] == TURF_SURFACE and not (horse_pps['pp_surface'] == TURF_SURFACE).any():
            if horse['bris_turf_pedigree_rating'] > horse.get('bris_dirt_pedigree_rating', 0) + PEDIGREE_IMPROVEMENT_THRESHOLD:
                adjustments['upgrade'][prog_num] = f"Strong turf pedigree ({horse['bris_turf_pedigree_rating']}) for first turf start"
        if horse['surface'] in WET_SURFACES and not (horse_pps['pp_track_condition'].isin(WET_TRACK_CONDITIONS)).any():
            if horse['bris_mud_pedigree_rating'] > horse.get('bris_dirt_pedigree_rating', 0) + PEDIGREE_IMPROVEMENT_THRESHOLD:
                adjustments['upgrade'][prog_num] = f"Strong mud pedigree ({horse['bris_mud_pedigree_rating']}) for first wet track start"

        if horse.get('tj_combo_roi_365d', 0) > TJ_COMBO_ROI_THRESHOLD and horse.get('tj_combo_starts_365d', 0) >= TJ_COMBO_MIN_STARTS:
            adjustments['upgrade'][prog_num] = f"High ROI T/J Combo ({horse['tj_combo_roi_365d']})"
    return adjustments

def adjust_groups_for_situation(initial_groups: Dict[str, List[Any]], contenders_df: pd.DataFrame, past_starts_df: pd.DataFrame) -> Tuple[Dict[str, List[Any]], Dict[str, Dict[Any, str]]]:
    """
    Adjusts contender groups based on pace, pedigree, and form analysis.
    Returns both the adjusted groups and the adjustments made.
    """
    race_num = contenders_df['race'].iloc[0]
    logger.info(f"--- Adjusting Groups for Race {race_num} ---")

    final_groups = {k: list(v) for k, v in initial_groups.items()}
    pace_scenario = analyze_pace_scenario(contenders_df)
    adjustments = get_situational_adjustments(contenders_df, past_starts_df, pace_scenario)

    for prog_num, reason in adjustments['upgrade'].items():
        if prog_num in final_groups['Group 2']:
            final_groups['Group 2'].remove(prog_num)
            final_groups['Group 1'].append(prog_num)
            logger.info(f"Upgrading horse #{prog_num} from Group 2 to 1. Reason: {reason}")
        elif prog_num in final_groups['Group 3']:
            final_groups['Group 3'].remove(prog_num)
            final_groups['Group 2'].append(prog_num)
            logger.info(f"Upgrading horse #{prog_num} from Group 3 to 2. Reason: {reason}")

    for prog_num, reason in adjustments['downgrade'].items():
        if prog_num in final_groups['Group 1']:
            final_groups['Group 1'].remove(prog_num)
            final_groups['Group 2'].append(prog_num)
            logger.info(f"Downgrading horse #{prog_num} from Group 1 to 2. Reason: {reason}")
        elif prog_num in final_groups['Group 2']:
            final_groups['Group 2'].remove(prog_num)
            final_groups['Group 3'].append(prog_num)
            logger.info(f"Downgrading horse #{prog_num} from Group 2 to 3. Reason: {reason}")

    for group in final_groups:
        final_groups[group] = sorted(list(set(final_groups[group])))

    logger.info(f"Final Adjusted Groups: {final_groups}")
    logger.info("--- Situational Analysis Complete ---")
    return final_groups, adjustments

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Running situational_analyzer.py in standalone mode for testing.")

    mock_contenders_data = {
        'program_number_if_available': ['1', '2', '3', '4', '5'],
        'race': [5, 5, 5, 5, 5],
        'bris_run_style_designation': ['E', 'P', 'S', 'E/P', 'P'],
        'surface': ['D', 'T', 'D', 'D', 'M'],
        'bris_dirt_pedigree_rating': [100, 80, 95, 90, 85],
        'bris_turf_pedigree_rating': [85, 105, 90, 88, 80],
        'bris_mud_pedigree_rating': [90, 85, 92, 91, 110],
        'tj_combo_roi_365d': [1.5, 0.8, 2.5, -0.5, 1.2],
        'tj_combo_starts_365d': [10, 12, 15, 20, 5]
    }
    mock_contenders_df = pd.DataFrame(mock_contenders_data)

    mock_pp_data = {
        'program_number_if_available': ['1', '2', '3', '4', '5'],
        'pp_surface': ['D', 'D', 'D', 'D', 'D'],
        'pp_track_condition': ['FT', 'FT', 'FT', 'FT', 'FT']
    }
    mock_past_starts_df = pd.DataFrame(mock_pp_data)

    initial_groups_mock = {
        "Group 1": ['1', '4'],
        "Group 2": ['2'],
        "Group 3": ['3', '5']
    }

    final_groups, adjustments = adjust_groups_for_situation(initial_groups_mock, mock_contenders_df, mock_past_starts_df)

    print("\n--- TEST RESULTS ---")
    print(f"Initial Groups: {initial_groups_mock}")
    print(f"Final Adjusted Groups: {final_groups}")
    print(f"Adjustments: {adjustments}")
