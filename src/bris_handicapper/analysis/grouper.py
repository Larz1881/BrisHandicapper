#!/usr/bin/env python
"""
Contender grouping module for the BrisHandicapper project.

This script implements Step 3 of the Adapted Handicapping Process, "The Keystone,"
which stratifies contenders into groups based on a "Factor Matrix" and "Gap Analysis"
of key performance indicators.
"""
import logging
import pandas as pd
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

# --- Configuration for Grouping Analysis ---
FACTOR_MATRIX_CONFIG = {
    'bris_prime_power': {
        'source_col': 'bris_prime_power',
        'source_df': 'current',
        'higher_is_better': True
    },
    'best_bris_speed': {
        'source_col': 'pp_bris_speed',
        'source_df': 'past',
        'higher_is_better': True
    },
    'best_2f_pace': {
        'source_col': 'pp_bris_pace_2f',
        'source_df': 'past',
        'higher_is_better': True
    },
    'best_4f_pace': {
        'source_col': 'pp_bris_pace_4f',
        'source_df': 'past',
        'higher_is_better': True
    },
    'best_late_pace': {
        'source_col': 'pp_bris_late_pace',
        'source_df': 'past',
        'higher_is_better': True
    }
}

SIGNIFICANT_GAPS = {
    'bris_prime_power': 5.0,
    'best_bris_speed': 5.0,
    'best_2f_pace': 3.0,
    'best_4f_pace': 3.0,
    'best_late_pace': 3.0
}

# --- Scoring and Grouping Constants ---
GAP_PENALTY = 3
GROUP_1_SIZE = 2
GROUP_2_SIZE = 2

def group_contenders(contenders_df: pd.DataFrame, past_starts_df: pd.DataFrame) -> Dict[str, List[Any]]:
    """
    Stratifies contenders into Groups 1, 2, and 3 based on gap analysis.
    """
    race_num = contenders_df['race_number'].iloc[0]
    logger.info(f"--- Grouping Contenders for Race {race_num} ---")

    if contenders_df.empty or len(contenders_df) < 2:
        logger.warning("Not enough contenders to perform grouping. Assigning all to Group 1.")
        return {"Group 1": contenders_df['program_number'].tolist(), "Group 2": [], "Group 3": []}

    factor_matrix = pd.DataFrame(index=contenders_df['program_number'])

    for factor, config in FACTOR_MATRIX_CONFIG.items():
        source_col = config['source_col']
        if config['source_df'] == 'current':
            factor_values = contenders_df.set_index('program_number')[source_col]
        else:
            relevant_pps = past_starts_df[past_starts_df['program_number'].isin(factor_matrix.index)]
            factor_values = relevant_pps.groupby('program_number')[source_col].max() if not relevant_pps.empty else pd.Series(dtype=float)
        factor_matrix[factor] = factor_values

    factor_matrix['grouping_score'] = 0
    for factor, config in FACTOR_MATRIX_CONFIG.items():
        if factor not in factor_matrix.columns or factor_matrix[factor].isnull().all():
            continue
        sorted_horses = factor_matrix[factor].sort_values(ascending=not config['higher_is_better']).dropna()
        if sorted_horses.empty:
            continue
        factor_matrix[f'{factor}_rank'] = sorted_horses.rank(method='min', ascending=False)
        factor_matrix['grouping_score'] += factor_matrix[f'{factor}_rank'].fillna(0)
        top_value = sorted_horses.iloc[0]
        gap_threshold = SIGNIFICANT_GAPS.get(factor, 5.0)
        horses_with_gap = sorted_horses[sorted_horses < (top_value - gap_threshold)].index
        if not horses_with_gap.empty:
            factor_matrix.loc[horses_with_gap, 'grouping_score'] += GAP_PENALTY

    sorted_scores = factor_matrix['grouping_score'].sort_values(ascending=True)
    logger.debug(f"Factor Matrix and Scores for Race {race_num}:\n{factor_matrix.to_string()}")

    favorite_prog_num = contenders_df.sort_values(by='morning_line_odds').iloc[0]['program_number']

    group1_candidates = set(sorted_scores.head(GROUP_1_SIZE).index)
    group1_candidates.add(favorite_prog_num)
    group1 = sorted(list(group1_candidates))

    remaining_contenders = sorted_scores.index.difference(group1)
    group2 = sorted(list(remaining_contenders[:GROUP_2_SIZE]))

    remaining_contenders = remaining_contenders.difference(group2)
    group3 = sorted(list(remaining_contenders))

    groups = {"Group 1": group1, "Group 2": group2, "Group 3": group3}
    logger.info(f"Final Groups for Race {race_num}: {groups}")
    logger.info("--- Contender Grouping Complete ---")
    return groups

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Running grouper.py in standalone mode for testing.")

    mock_contenders_data = {
        'track_code': ['TEST'] * 5,
        'race_number': [5] * 5,
        'program_number': ['1', '2', '3', '4', '5'],
        'horse_name': ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo'],
        'morning_line_odds': [2.0, 3.0, 10.0, 5.0, 12.0],
        'bris_prime_power': [145.0, 148.0, 130.0, 144.0, 125.0],
    }
    mock_contenders_df = pd.DataFrame(mock_contenders_data)

    mock_pp_data = {
        'program_number': ['1', '1', '2', '2', '3', '3', '4', '4', '5', '5'],
        'pp_bris_speed': [95, 100, 98, 99, 85, 86, 96, 97, 80, 82],
        'pp_bris_pace_2f': [90, 92, 95, 96, 80, 81, 88, 89, 75, 76],
        'pp_bris_pace_4f': [100, 101, 98, 99, 90, 91, 95, 96, 85, 86],
        'pp_bris_late_pace': [95, 96, 96.5, 97.5, 85, 86, 91.5, 92.5, 80, 81]
    }
    mock_pp_df = pd.DataFrame(mock_pp_data)

    final_groups = group_contenders(mock_contenders_df, mock_pp_df)

    print("\n--- TEST RESULTS ---")
    print(f"Initial Contenders: {mock_contenders_df['program_number'].tolist()}")
    print(f"Final Groups: {final_groups}")
