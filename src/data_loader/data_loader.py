import pandas as pd
from pathlib import Path
# Use a relative import to access the centralized path configuration
from ..config.paths import RAW_DATA_DIR

def load_parquet_data(file_name: str) -> pd.DataFrame:
    """
    Loads a Parquet file from the data/raw directory into a pandas DataFrame.

    Args:
        file_name (str): The name of the Parquet file (e.g., "parsed_race_data_full.parquet").

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame.

    Raises:
        FileNotFoundError: If the specified Parquet file does not exist.
        Exception: For other errors during file loading.
    """
    data_file_path = RAW_DATA_DIR / file_name

    if not data_file_path.is_file():
        raise FileNotFoundError(f"Parquet file not found at: {data_file_path}")

    try:
        df = pd.read_parquet(data_file_path)
        print(f"Successfully loaded {file_name} from {data_file_path}")
        return df
    except Exception as e:
        raise Exception(f"Error loading Parquet file {file_name}: {e}")

if __name__ == '__main__':
    # Example usage (for testing purposes)
    # To run this script directly for testing, you might need to adjust the python path
    # to resolve the relative import. It's better to run it as a module from the
    # project root, e.g., by running the following command from the BrisHandicapper directory:
    # python -m src.data_loader.data_loader
    try:
        # Assuming 'parsed_race_data_full.parquet' is in data/raw
        df_parsed_data = load_parquet_data("parsed_race_data_full.parquet")
        print(f"Loaded parsed_race_data_full.parquet with shape: {df_parsed_data.shape}")
        # print(df_parsed_data.head()) # Uncomment to see the first few rows

    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
