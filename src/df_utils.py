from datetime import date

import numpy as np
import pandas as pd
import statsmodels.api as sm

from extract import extract
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
    df["fecha"] = pd.to_datetime(df["fecha"], dayfirst=True)

    # Sort the df by date
    df.sort_values(by=["fecha"], inplace=True)
    df.set_index("fecha", inplace=True)

    df = df.apply(pd.to_numeric, errors="coerce")

    return df


def save(df, prefix="", index=False):
    """
    Stores the DataFrame in a CSV file with today's date appended to the filename.

    Parameters:
        df (DataFrame): Input DataFrame.
        prefix (str, optional): Prefix to be added to the filename. Default is an empty string.
        index (bool, optional): Whether to include the index in the CSV file. Default is False.
    """
    today = date.today().strftime("%Y_%m_%d")
    df.to_csv(f"data/{prefix+today}.csv", index=index)

    return df


def set_date_index(df):
    """
    Preprocess the DataFrame by converting the 'fecha' column to datetime and setting it as index.

    Parameters:
        df (DataFrame): Input DataFrame.

    Returns:
        DataFrame: Preprocessed DataFrame with date index.
    """
    df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y")
    df.set_index("fecha", inplace=True)
    return df


def filter_dates_with_day_01(df):
    """
    Filter DataFrame to only include rows with dates that have day 01.

    Parameters:
        df (DataFrame): Input DataFrame with date index.

    Returns:
        DataFrame: Filtered DataFrame containing rows with dates having day 01.
    """
    filtered_df = df[df.index.day == 1]
    return filtered_df


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
            print(f"Error on X13-ARIMA with series {column}: ", e)
        else:
            # Replace the original series with the trend component
            df_stationarized.loc[:, column] = x13_result.trend

    return df_stationarized


def remove_outliers(df, threshold=10):
    """
    Removes outliers from all columns of a DataFrame using the IQR method.

    Parameters:
        df (DataFrame): Input DataFrame.
        threshold (float, optional): Multiplier for the IQR to determine outliers. Default is 1.5.

    Returns:
        DataFrame: DataFrame with outliers changed to 0.
    """
    df_no_outliers = df.copy()

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            df_no_outliers[col] = df_no_outliers[col].apply(
                lambda x: 0 if x < lower_bound or x > upper_bound else x
            )

    return df_no_outliers


def fillna_with_zero(df):
    """
    Fills NaN values in all columns of a DataFrame with 0.

    Parameters:
        df (DataFrame): Input DataFrame.

    Returns:
        DataFrame: DataFrame with NaN values replaced with 0.
    """
    return df.fillna(0)


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
    settings = read_yaml("src/settings.yaml")
    series = {key: value for key, value in settings.items() if key != "base_url"}

    df_transformed = df.copy()

    for serie, info in series.items():
        df_transformed[serie] = df_transformed[serie].apply(
            lambda x: transformation(info["transformation"], x)
        )

    return df_transformed


def create_quarterly_data(df):

    # Resample the DataFrame to quarterly frequency
    quarterly_df = df.resample(
        "QS"
    ).mean()  # You can use other methods like sum(), median(), etc. instead of mean() if needed

    # Forward fill missing values if any
    quarterly_df = quarterly_df.ffill()

    return quarterly_df


def add_indicators(df):
    indicators = read_yaml("src/indicators.yaml")

    ind_df = extract(indicators)

    # Replacing '01/02' with '01/04' in the 'dates' column
    ind_df["fecha"] = ind_df["fecha"].str.replace("01/04", "01/10")
    ind_df["fecha"] = ind_df["fecha"].str.replace("01/03", "01/07")
    ind_df["fecha"] = ind_df["fecha"].str.replace("01/02", "01/04")
    ind_df = set_date_index(ind_df)
    merged_df = df.merge(ind_df, left_index=True, right_index=True, how='left')


    return merged_df
