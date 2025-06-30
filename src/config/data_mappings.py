# BrisHandicapper/src/config/data_mappings.py

# This dictionary maps raw column names from the input Parquet files
# (derived from bris_dict.txt) to more readable and consistent names
# used within the application.

COLUMN_MAPPINGS = {
    # --- Today's Race Data (Current Race Info) ---
    "Track": "track_code",
    "Date": "race_date_today",
    "Race_#": "race_number",
    "Post_Position": "post_position_today",
    "Distance_(in_yards)": "distance_yards",
    "Surface": "surface_today",
    "Race_Type": "race_type_today",
    "Age/Sex_Restrictions": "age_sex_restrictions_today",
    "Purse": "purse_today",
    "Claiming_Price": "claiming_price_today",
    "2f_BRIS_Pace_Par_for_level": "par_pace_2f",
    "4f_BRIS_Pace_Par_for_level": "par_pace_4f",
    "6f_BRIS_Pace_Par_for_level": "par_pace_6f",
    "BRIS_Speed_Par_for_class_level": "par_speed",
    "BRIS_Late_Pace_Par_for_level": "par_late_pace",

    # --- Today's Horse/Trainer/Jockey/Owner (Current Race Info) ---
    "Horse_Name": "horse_name",
    "Program_Number_(if_available)": "program_number",
    "Morn._Line_Odds(if_available)": "morning_line_odds",
    "Today's_Jockey": "jockey_name",
    "Today's_Trainer": "trainer_name",
    "Weight": "assigned_weight",
    "Today's_Medication": "medication_today",
    "Equipment_Change": "equipment_change_today",
    "BRIS_Run_Style_designation": "bris_run_style",
    ""Quirin"_style_Speed_Points": "quirin_speed_points",
    "BRIS_Prime_Power_Rating": "bris_prime_power",
    "#_of_days_since_last_race": "days_since_last_race",

    # --- Horse History Data (Current Race Info - Pedigree) ---
    "Sire": "sire_name",
    "Dam": "dam_name",
    "Dam's_sire": "dam_sire_name",
    "BRIS_Dirt_Pedigree_Rating": "bris_ped_dirt",
    "BRIS_Mud_Pedigree_Rating": "bris_ped_mud",
    "BRIS_Turf_Pedigree_Rating": "bris_ped_turf",
    "BRIS_Dist_Pedigree_Rating": "bris_ped_distance",
    "Sire_Stud_Fee_(current)": "sire_stud_fee",
    "Auction_Price": "auction_price",

    # --- Trainer/Jockey Stats (Current Race Info) ---
    "Trainer_Sts_Current_Meet": "trainer_starts_meet",
    "Trainer_Wins_Current_Meet": "trainer_wins_meet",
    "Trainer_Places_Current_Meet": "trainer_places_meet",
    "Trainer_Shows_Current_Meet": "trainer_shows_meet",
    "Jockey_Sts_Current_Meet": "jockey_starts_meet",
    "Jockey_Wins_Current_Meet": "jockey_wins_meet",
    "Jockey_Places_Current_Meet": "jockey_places_meet",
    "Jockey_Shows_Current_Meet": "jockey_shows_meet",
    "T/J_Combo_#_Starts_(365D)": "tj_combo_starts_365d",
    "T/J_Combo_#_Wins_(365D)": "tj_combo_wins_365d",
    "T/J_Combo_#_Places_(365D)": "tj_combo_places_365d",
    "T/J_Combo_#_Shows_(365D)": "tj_combo_shows_365d",
    "T/J_Combo_$2_ROI_(365D)": "tj_combo_roi_365d",
    "Trainer_Sts_Current_Year": "trainer_starts_year",
    "Trainer_Wins_Current_Year": "trainer_wins_year",
    "Trainer_Places_Current_Year": "trainer_places_year",
    "Trainer_Shows_Current_Year": "trainer_shows_year",
    "Trainer_ROI_Current_Year": "trainer_roi_year",
    "Jockey_Sts_Current_Year": "jockey_starts_year",
    "Jockey_Wins_Current_Year": "jockey_wins_year",
    "Jockey_Places_Current_Year": "jockey_places_year",
    "Jockey_Shows_Current_Year": "jockey_shows_year",
    "Jockey_ROI_Current_Year": "jockey_roi_year",

    # --- Horse's Past Performance Data (parsed_race_data_full.parquet) ---
    # Assuming a suffix _N for the Nth past race (1-10, 1 being most recent)
    # This section will require careful mapping based on actual parquet column names.
    # The bris_dict.txt shows ranges like 256-265 for Race Date, implying Race_Date_1, Race_Date_2 etc.
    # I'll provide a template for the first few, and you can extend based on your actual data.

    # Example for 1st past race (most recent)
    "Race_Date_1": "pp_race_date_1",
    "Track_Code_1": "pp_track_code_1",
    "Distance_(in_yards)_1": "pp_distance_yards_1",
    "Surface_1": "pp_surface_1",
    "Track_Condition_1": "pp_track_condition_1",
    "Final_Time_1": "pp_final_time_1",
    "Fraction_#1_1": "pp_fraction_1_time_1",
    "Fraction_#2_1": "pp_fraction_2_time_1",
    "Fraction_#3_1": "pp_fraction_3_time_1",
    "Finish_Position_1": "pp_finish_position_1",
    "Finish_BtnLngths_only_1": "pp_finish_lengths_behind_1",
    "BRIS_Speed_Rating_1": "pp_bris_speed_1",
    "BRIS_2f_Pace_Fig_1": "pp_bris_pace_2f_1",
    "BRIS_4f_Pace_Fig_1": "pp_bris_pace_4f_1",
    "BRIS_6f_Pace_Fig_1": "pp_bris_pace_6f_1",
    "BRIS_Late_Pace_Fig_1": "pp_bris_late_pace_1",
    "BRIS_Race_Shape_-_1st_Call_1": "pp_bris_race_shape_1c_1",
    "BRIS_Race_Shape_-_2nd_Call_1": "pp_bris_race_shape_2c_1",

    # ... extend for _2 to _10 for all relevant past performance fields
    # You will need to inspect your actual parquet file's column names for these.
}

# Example of how to generate mappings for all 10 past performances if they follow a consistent suffix pattern
def generate_pp_mappings(num_pps=10):
    pp_map = {}
    base_pp_fields = {
        "Race_Date": "pp_race_date",
        "Track_Code": "pp_track_code",
        "Distance_(in_yards)": "pp_distance_yards",
        "Surface": "pp_surface",
        "Track_Condition": "pp_track_condition",
        "Final_Time": "pp_final_time",
        "Fraction_#1": "pp_fraction_1_time",
        "Fraction_#2": "pp_fraction_2_time",
        "Fraction_#3": "pp_fraction_3_time",
        "Finish_Position": "pp_finish_position",
        "Finish_BtnLngths_only": "pp_finish_lengths_behind",
        "BRIS_Speed_Rating": "pp_bris_speed",
        "BRIS_2f_Pace_Fig": "pp_bris_pace_2f",
        "BRIS_4f_Pace_Fig": "pp_bris_pace_4f",
        "BRIS_6f_Pace_Fig": "pp_bris_pace_6f",
        "BRIS_Late_Pace_Fig": "pp_bris_late_pace",
        "BRIS_Race_Shape_-_1st_Call": "pp_bris_race_shape_1c",
        "BRIS_Race_Shape_-_2nd_Call": "pp_bris_race_shape_2c",
    }
    for i in range(1, num_pps + 1):
        for raw_name, mapped_name_base in base_pp_fields.items():
            pp_map[f"{raw_name}_{i}"] = f"{mapped_name_base}_{i}"
    return pp_map

# Merge generated PP mappings into the main COLUMN_MAPPINGS
COLUMN_MAPPINGS.update(generate_pp_mappings())
