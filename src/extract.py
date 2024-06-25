import logging
from datetime import date

import pandas as pd

from utils import *


def extract(series):
    """
    Extracts the data from the API and merges it into a single DataFrame.
    It also creates a log with possible warnings during this process.

    Parameters:
        base_url (str): The base URL of the API.
        series (list): List of series identifiers to retrieve data from the API.

    Returns:
        DataFrame: Merged DataFrame containing data from all series.

    Notes:
        This function retrieves data from the API for the given list of series identifiers
        and merges them into a single DataFrame. It creates a log file to record any
        warnings or errors encountered during the extraction process.
    """
    # Create the log
    logging.basicConfig(
        filename=f"log/{date.today().strftime('%Y_%m_%d')}.log",
        filemode="w",
        level=logging.INFO,
    )

    # Initialize an empty DataFrame
    df = pd.DataFrame()

    for serie, info in series.items():

        try:
            if info["source"] == "banxico":
                # Retrieve data for the series
                temp_df = data_from_banxico(serie)
            else:
                temp_df = data_from_inegi(serie)

            # Handle the first series separately to initialize the DataFrame
            if df.empty:
                df = temp_df
            else:
                # Merge the series into the DataFrame
                df = df.merge(temp_df, on="fecha", how="outer")

            # Check if the series is not outdated (last observation is last month)
            last_observation_date = temp_df["fecha"].iloc[-1]
            if not is_outdated(last_observation_date):
                logging.warning(f"Serie:{serie} seems to be outdated")

        except Exception as e:
            # Log any errors encountered during the extraction process
            logging.error(f"Serie {serie} could not be retrieved: {e}")

    # Apply transformations after merging all series
    df = df.applymap(remove_ne).applymap(remove_commas)

    return df

