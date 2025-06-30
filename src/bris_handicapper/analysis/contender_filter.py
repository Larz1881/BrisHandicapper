#!/usr/bin/env python
"""
Contender identification module for the BrisHandicapper project.

This script implements Step 2 of the Adapted Handicapping Process, filtering
the field to identify legitimate contenders based on a set of predefined rules.
"""
import logging
import pandas as pd
from typing import List, Set

logger = logging.getLogger(__name__)

# --- Rule Configuration Constants ---
PRIME_POWER_RANK_THRESHOLD = 4
COMPETITIVE_SPEED_POINT_DIFFERENCE = 5
PACE_FIGURE_RANK_THRESHOLD = 3
PEDIGREE_RATING_IMPROVEMENT_THRESHOLD = 5
RECENT_RACE_COUNT = 3

def get_top_last_race_speed(race_df: pd.DataFrame, past_starts_df: pd.DataFrame) -> float:
    """
    Finds the highest Brisnet Speed Rating from any horse's most recent race.
    """
    race_horses = race_df['program_number'].unique()
    relevant_pps = past_starts_df[past_starts_df['program_number'].isin(race_horses)]
    if relevant_pps.empty:
        return 0
    last_races = relevant_pps.loc[relevant_pps.groupby('program_number')['pp_race_date'].idxmax()]
    if 'pp_bris_speed' in last_races.columns and not last_races['pp_bris_speed'].isnull().all():
        return last_races['pp_bris_speed'].max()
    return 0

def isolate_contenders(race_df: pd.DataFrame, past_starts_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters a race's full field to identify and return only legitimate contenders.
    """
    race_num = race_df['race_number'].iloc[0]
    logger.info(f"--- Isolating Contenders for Race {race_num} ---")
    if race_df.empty:
        logger.warning("Input race_df is empty. Cannot identify contenders.")
        return pd.DataFrame()

    contenders = set()

    # Rule 1: Top Tier Prime Power
    top_prime_power = race_df.nlargest(PRIME_POWER_RANK_THRESHOLD, 'bris_prime_power')
    new_contenders = set(top_prime_power['program_number'].unique()) - contenders
    if new_contenders:
        logger.debug(f"Rule 1 (Prime Power) adds: {new_contenders}")
        contenders.update(new_contenders)

    # Rule 2: Competitive Speed
    top_speed_benchmark = get_top_last_race_speed(race_df, past_starts_df)
    speed_threshold = top_speed_benchmark - COMPETITIVE_SPEED_POINT_DIFFERENCE
    race_horses = race_df['program_number'].unique()
    relevant_pps = past_starts_df[past_starts_df['program_number'].isin(race_horses)]
    last_three_races = relevant_pps.groupby('program_number').tail(RECENT_RACE_COUNT)
    competitive_speed_horses = last_three_races[last_three_races['pp_bris_speed'] >= speed_threshold]
    new_contenders = set(competitive_speed_horses['program_number'].unique()) - contenders
    if new_contenders:
        logger.debug(f"Rule 2 (Competitive Speed >= {speed_threshold}) adds: {new_contenders}")
        contenders.update(new_contenders)

    # Rule 3: Pace Advantage
    pace_figures = ['pp_bris_pace_2f', 'pp_bris_pace_4f', 'pp_bris_late_pace']
    for fig in pace_figures:
        if fig in relevant_pps.columns:
            best_pace_per_horse = relevant_pps.groupby('program_number')[fig].max().nlargest(PACE_FIGURE_RANK_THRESHOLD)
            new_contenders = set(best_pace_per_horse.index) - contenders
            if new_contenders:
                logger.debug(f"Rule 3 (Top {PACE_FIGURE_RANK_THRESHOLD} in {fig}) adds: {new_contenders}")
                contenders.update(new_contenders)

    # Rule 4: Pedigree Potential
    for _, horse in race_df.iterrows():
        prog_num = horse['program_number']
        horse_pps = past_starts_df[past_starts_df['program_number'] == prog_num]
        # Turf Switch
        if horse['surface'] == 'T' and not (horse_pps['pp_surface'] == 'T').any():
            if horse['bris_ped_turf'] > horse.get('bris_ped_dirt', 0) + PEDIGREE_RATING_IMPROVEMENT_THRESHOLD:
                if prog_num not in contenders:
                    logger.debug(f"Rule 4 (Pedigree) adds #{prog_num} for Turf switch.")
                    contenders.add(prog_num)
        # Wet Track Switch
        if horse['surface'] in ['M', 'S'] and not (horse_pps['pp_track_condition'].isin(['M', 'S', 'SY'])).any():
            if horse['bris_ped_mud'] > horse.get('bris_ped_dirt', 0) + PEDIGREE_RATING_IMPROVEMENT_THRESHOLD:
                if prog_num not in contenders:
                    logger.debug(f"Rule 4 (Pedigree) adds #{prog_num} for Wet Track.")
                    contenders.add(prog_num)

    if not contenders:
        logger.warning(f"No contenders were identified for Race {race_num} based on the rules.")
        return pd.DataFrame()

    final_contenders_df = race_df[race_df['program_number'].isin(contenders)].copy()
    logger.info(f"Identified {len(final_contenders_df)} contenders for Race {race_num}: {sorted(list(contenders))}")
    logger.info("--- Contender Isolation Complete ---")
    return final_contenders_df

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Running contender_filter.py in standalone mode for testing.")

    mock_race_data = {
        'track_code': ['TEST']*6,
        'race_number': [5]*6,
        'program_number': ['1', '2', '3', '4', '5', '6'],
        'horse_name': ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot'],
        'bris_prime_power': [145, 142, 140, 135, 130, 128],
        'surface': ['D', 'D', 'T', 'M', 'D', 'T'],
        'bris_ped_dirt': [100, 105, 90, 85, 95, 80],
        'bris_ped_turf': [80, 85, 110, 80, 90, 95],
        'bris_ped_mud': [90, 85, 80, 115, 70, 75]
    }
    mock_race_df = pd.DataFrame(mock_race_data)

    mock_past_starts_data = {
        'program_number': ['1', '1', '1', '2', '2', '2', '3', '3', '4', '4', '5', '5', '6', '6'],
        'pp_race_date': pd.to_datetime(['2024-01-01', '2024-02-01', '2024-03-01', '2024-01-15', '2024-02-15', '2024-03-15', '2024-01-20', '2024-02-20', '2024-01-10', '2024-02-10', '2024-01-25', '2024-02-25', '2024-01-18', '2024-02-18']),
        'pp_bris_speed': [95, 92, 98, 90, 94, 91, 85, 88, 89, 92, 80, 82, 70, 75],
        'pp_bris_pace_2f': [90, 92, 91, 99, 86, 84, 80, 82, 81, 83, 75, 76, 98, 97],
        'pp_bris_pace_4f': [88, 89, 90, 92, 93, 91, 95, 96, 94, 95, 85, 86, 88, 87],
        'pp_bris_late_pace': [93, 94, 95, 85, 86, 87, 98, 99, 90, 91, 92, 93, 80, 81],
        'pp_surface': ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],
        'pp_track_condition': ['FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'FT', 'SY', 'M']
    }
    mock_pp_df = pd.DataFrame(mock_past_starts_data)

    contenders = isolate_contenders(mock_race_df, mock_pp_df)

    print("\n--- TEST RESULTS ---")
    if not contenders.empty:
        print("Identified Contenders:")
        print(contenders[['program_number', 'horse_name']])
    else:
        print("No contenders identified.")
