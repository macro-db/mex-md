import pandas as pd

from datetime import date


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


def load(df, prefix='', index=False):
    """
    Stores the DataFrame in a CSV file with today's date appended to the filename.

    Parameters:
        df (DataFrame): Input DataFrame.
        prefix (str, optional): Prefix to be added to the filename. Default is an empty string.
        index (bool, optional): Whether to include the index in the CSV file. Default is False.
    """
    today = date.today().strftime("%Y_%m_%d")
    df.to_csv(f'data/{prefix+today}.csv', index=index)