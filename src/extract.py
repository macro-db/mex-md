import pandas as pd
import logging

from datetime import date

from utils import *


def extract():
    """
    Extracts the data from the API and merges it into a single df.
    It also creates a log with possible warnings in this step

    Parameters:
        df (DataFrame): Input DataFrame.
        column_names (list): List of column names to detect outliers from.
        threshold (float): Multiplier for the IQR to determine outliers. Default is 1.5.

    Returns:
        DataFrame: DataFrame with outliers removed.
    """
    # Create the log
    logging.basicConfig(filename=f"log/{date.today().strftime('%Y_%m_%d')}.log", filemode="w", level=logging.INFO)

    # Read yaml file containing the base url, and the series ID, transformation, and desired name in the df
    settings = read_yaml("src/settings_test.yaml")
    base_url = settings['base_url']
    series = [key for key in settings.keys() if key != 'base_url']

    # Get the first series to create an initial df
    first_serie = series[0]
    df = pd.DataFrame(data_from_series(base_url, first_serie)['datos'])
    df.rename(columns={"dato": first_serie}, inplace=True)

    # Merge the rest of series into the df, joined by the date column
    for serie in series[1:]:
        try:
            temp_df = pd.DataFrame(data_from_series(base_url, serie)['datos'])
        
        #If the series is not retrieved, handle the error, and log it
        except Exception:
            logging.error(f'Serie{serie} could not be retreived')
        
        #For the retrieved series, format the n/e and commas, and merge it 
        else:
            temp_df.rename(columns={"dato": serie}, inplace=True)
            temp_df[serie] = temp_df[serie].transform(remove_ne)
            temp_df[serie] = temp_df[serie].transform(remove_commas)

            # Check if the series is not outdated (last observation is last month)
            last_observation_date = temp_df['fecha'].iloc[-1]
            if not is_last_month(last_observation_date):
                logging.warning(f"Serie:{serie} seems to be outdated")
            
            df = df.merge(temp_df, on='fecha', how='outer')

    return df
