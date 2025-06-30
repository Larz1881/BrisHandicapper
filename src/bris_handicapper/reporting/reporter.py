#!/usr/bin/env python
"""
Reporting module for the BrisHandicapper project.

This script implements Step 6 of the Adapted Handicapping Process. It takes the
final analysis results and generates a structured report, optimized for
consumption by a Large Language Model (LLM) for final takeaway generation.
"""
import logging
import json
from pathlib import Path
import pandas as pd
from typing import Dict, List, Any

from src.bris_handicapper.config import settings
from src.bris_handicapper.analysis.grouper import FACTOR_MATRIX_CONFIG

logger = logging.getLogger(__name__)

def build_factor_matrix_for_report(
    contenders_df: pd.DataFrame, past_starts_df: pd.DataFrame
) -> Dict[str, Dict[str, Any]]:
    """
    Builds a data-rich dictionary of the key performance factors for top contenders.
    """
    report_matrix = {}
    program_numbers = contenders_df['program_number'].tolist()
    
    for prog_num in program_numbers:
        horse_data = contenders_df[contenders_df['program_number'] == prog_num].iloc[0]
        horse_pps = past_starts_df[past_starts_df['program_number'] == prog_num]
        
        horse_report = {}
        for factor, config in FACTOR_MATRIX_CONFIG.items():
            source_col = config['source_col']
            if config['source_df'] == 'current':
                value = horse_data.get(source_col)
            else:
                value = horse_pps[source_col].max() if not horse_pps.empty else None
            
            horse_report[factor] = round(value, 2) if pd.notnull(value) else 'N/A'
            
        report_matrix[prog_num] = horse_report
        
    return report_matrix

def generate_llm_report_data(
    final_groups: Dict[str, List[Any]],
    contenders_df: pd.DataFrame,
    past_starts_df: pd.DataFrame,
    adjustments: Dict[str, Dict[Any, str]]
) -> Dict[str, Any]:
    """
    Generates a structured dictionary for a single race, optimized for an LLM.
    """
    race_info = contenders_df.iloc[0]
    track_id = race_info['track_code']
    race_num = race_info['race_number']
    
    favorite = contenders_df.sort_values(by='morning_line_odds').iloc[0]
    favorite_prog_num = favorite['program_number']
    
    if favorite_prog_num in final_groups.get("Group 1", []):
        favorite_status = "Legitimate"
    elif favorite_prog_num in final_groups.get("Group 2", []):
        favorite_status = "Vulnerable"
    else:
        favorite_status = "False"

    win_candidates = final_groups.get("Group 1", [])
    top_plays = [p for p in win_candidates if p != favorite_prog_num]
    key_horse = top_plays[0] if top_plays else None

    report = {
        "race_identification": {
            "track": track_id,
            "race_number": int(race_num),
            "distance_furlongs": round(race_info.get('distance_yards', 0) / 220, 2),
            "surface": race_info.get('surface'),
            "race_type": race_info.get('race_type')
        },
        "handicapping_summary": {
            "favorite_details": {
                "program_number": favorite_prog_num,
                "name": favorite['horse_name'],
                "classification": favorite_status
            },
            "key_horse_for_exotics": key_horse,
            "primary_win_contenders": top_plays,
            "contender_groups": final_groups
        },
        "supporting_data": {
            "factor_matrix": build_factor_matrix_for_report(contenders_df, past_starts_df),
            "adjustment_notes": adjustments
        },
        "metadata": {
            "report_generated_at": pd.Timestamp.now().isoformat(),
            "process": "BrisHandicapper Adapted Handicapping Process"
        }
    }
    return report

def save_report(report_data: Dict[str, Any], output_dir: Path):
    """Saves the report data as a JSON file."""
    track = report_data["race_identification"]["track"]
    race_num = report_data["race_identification"]["race_number"]
    
    track_dir = output_dir / track
    track_dir.mkdir(exist_ok=True)
    
    file_path = track_dir / f"race_{race_num}_report.json"
    
    try:
        with open(file_path, 'w') as f:
            json.dump(report_data, f, indent=4)
        logger.info(f"Successfully saved report to: {file_path}")
    except Exception as e:
        logger.error(f"Failed to save report to {file_path}: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Running reporter.py in standalone mode for testing.")

    mock_contenders_data = {
        'track_code': ['TEST'] * 4,
        'race_number': [5] * 4,
        'program_number': ['1', '2', '7', '8'],
        'horse_name': ['Alpha', 'Bravo', 'Charlie', 'Delta'],
        'morning_line_odds': [2.0, 3.0, 5.0, 8.0],
        'distance_yards': [1760, 1760, 1760, 1760],
        'surface': ['T', 'T', 'T', 'T'],
        'race_type': ['A', 'A', 'A', 'A'],
        'bris_prime_power': [145, 148, 144, 130]
    }
    mock_contenders_df = pd.DataFrame(mock_contenders_data)

    mock_pp_data = {
        'program_number': ['1', '2', '7', '8'],
        'pp_bris_speed': [100, 99, 97, 86],
        'pp_bris_pace_2f': [92, 96, 88, 81],
        'pp_bris_pace_4f': [101, 99, 96, 90],
        'pp_bris_late_pace': [96, 97.5, 92.5, 85]
    }
    mock_pp_df = pd.DataFrame(mock_pp_data)

    final_groups_mock = {"Group 1": ['2', '7'], "Group 2": ['1'], "Group 3": ['8']}
    
    mock_adjustments = {
        'upgrade': {'7': 'Advantaged by Pace Duel scenario'},
        'downgrade': {'1': 'Disadvantaged by Pace Duel scenario'}
    }

    report_json = generate_llm_report_data(final_groups_mock, mock_contenders_df, pd.DataFrame(mock_pp_data), mock_adjustments)

    print("\n--- LLM-Optimized JSON Output ---")
    print(json.dumps(report_json, indent=4))
    
    test_output_dir = Path("./reports_test")
    test_output_dir.mkdir(exist_ok=True)
    save_report(report_json, test_output_dir)
