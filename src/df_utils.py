import pandas as pd
import numpy as np
import statsmodels.api as sm

from datetime import date

from utils import read_yaml


def order(df):
    """
    Orders the raw dataset by date.

    Parameters:
        df (DataFrame): Input DataFrame.

    Returns:
        DataFrame: DataFrame with ordered rows.
    """
    # Change the date to datetime to be able to order the rows
    df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)

    #Sort the df by date
    df.sort_values(by=['fecha'], inplace=True)

    #Change back to string to preserve the raw data format
    df['fecha'] = df['fecha'].dt.strftime('%d/%m/%Y')
        
    return df


def save(df, prefix='', index=False):
    """
    Stores the DataFrame in a CSV file with today's date appended to the filename.

    Parameters:
        df (DataFrame): Input DataFrame.
        prefix (str, optional): Prefix to be added to the filename. Default is an empty string.
        index (bool, optional): Whether to include the index in the CSV file. Default is False.
    """
    today = date.today().strftime("%Y_%m_%d")
    df.to_csv(f'data/{prefix+today}.csv', index=index)

    return df


def set_date_index(df):
    """
    Preprocess the DataFrame by converting the 'fecha' column to datetime and setting it as index.

    Parameters:
        df (DataFrame): Input DataFrame.

    Returns:
        DataFrame: Preprocessed DataFrame with date index.
    """
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')
    df.set_index('fecha', inplace=True)
    return df


def slice_df_from_date(df, start_date):
    """
    Slice the DataFrame to get data from the specified start date onwards.

    Parameters:
    df (pandas.DataFrame): The DataFrame to be sliced.
    start_date (str): The start date from which to slice the DataFrame (format: 'YYYY-MM-DD').

    Returns:
    pandas.DataFrame: Sliced DataFrame starting from the specified start date.
    """
    return df[start_date:]


def stationarize_df(df, series):
    """
    Stationarize the specified series in the DataFrame using X13-ARIMA analysis.

    Parameters:
        df (DataFrame): Input DataFrame.
        series (list): List of column names to stationarize.

    Returns:
        None
    """
    # Make a copy of the original DataFrame
    df_stationarized = df.copy()

    # Apply x13_arima_analysis to each series
    for column in series:
        try:
            # Perform X13-ARIMA analysis
            x13_result = sm.tsa.x13_arima_analysis(df[column], x12path="x13as")
        except Exception as e:
            print(f'Error on X13-ARIMA with series {column}: ', e)
        else:
            # Replace the original series with the trend component
            df_stationarized.loc[:, column] = x13_result.trend

    return df_stationarized


def remove_outliers(df, column_names, threshold=1.5):
    """
    Removes outliers from specified columns of a DataFrame using the IQR method.

    Parameters:
        df (DataFrame): Input DataFrame.
        column_names (list): List of column names to detect outliers from.
        threshold (float): Multiplier for the IQR to determine outliers. Default is 1.5.

    Returns:
        DataFrame: DataFrame with outliers removed.
    """
    # Make a copy of the original DataFrame
    df_filtered = df.copy()
    
    for column_name in column_names:
        # Calculate quartiles and IQR
        q1 = df[column_name].quantile(0.25)
        q3 = df[column_name].quantile(0.75)
        IQR = q3 - q1

        # Calculate lower and upper bounds for outlier detection
        lower_bound = q1 - threshold * IQR
        upper_bound = q3 + threshold * IQR

        # Filter DataFrame to remove outliers
        df_filtered = df_filtered[(df_filtered[column_name] >= lower_bound) & (df_filtered[column_name] <= upper_bound)]
    
    return df_filtered
    

def transformation(tcode, x):
    small = 1e-10  # Defined small value for logs

    if tcode == 1:  # Level (no transformation)
        y = x

    elif tcode == 2:  # First difference
        y = np.diff(x, axis=0)

    elif tcode == 3:  # Second difference
        y = np.diff(x, n=2, axis=0)

    elif tcode == 4:  # Natural log
        y = np.where(np.min(x) < small, np.nan, np.log(x))

    else:
        raise ValueError("Invalid transformation code")

    return y

def apply_transformations(df):
    settings = read_yaml("src/settings_test.yaml")
    series = {key: value for key, value in settings.items() if key != 'base_url'}

    df_transformed = df.copy()

    for serie, info in series.items():
        df_transformed[serie] = df_transformed[serie].apply(lambda x: transformation(info['transformation'], x))
    
    return df_transformed