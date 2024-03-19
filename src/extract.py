import pandas as pd
import logging

from datetime import date

from utils import *


def extract(base_url, series):
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
    logging.basicConfig(filename=f"log/{date.today().strftime('%Y_%m_%d')}.log", filemode="w", level=logging.INFO)

    # Initialize an empty DataFrame
    df = pd.DataFrame()

    for serie in series:
        try:
            # Retrieve data for the series
            temp_df = pd.DataFrame(data_from_series(base_url, serie)['datos'])
            
            # Handle the first series separately to initialize the DataFrame
            if df.empty:
                df = temp_df.rename(columns={"dato": serie})
            else:
                # Merge the series into the DataFrame
                temp_df.rename(columns={"dato": serie}, inplace=True)
                df = df.merge(temp_df, on='fecha', how='outer')

            # Check if the series is not outdated (last observation is last month)
            last_observation_date = temp_df['fecha'].iloc[-1]
            if not is_last_month(last_observation_date):
                    logging.warning(f"Serie:{serie} seems to be outdated")

        except Exception as e:
            # Log any errors encountered during the extraction process
            logging.error(f'Serie {serie} could not be retrieved: {e}')
        
    # Apply transformations after merging all series
    df = df.applymap(remove_ne).applymap(remove_commas)

    return df