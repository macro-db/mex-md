import statsmodels.api as sm
import pandas as pd


def stationarize_panel(df, series):
    # Apply x13_arima_analysis to each series
    for column in series:
        try:
            x13_result = sm.tsa.x13_arima_analysis(df[column], x12path = "x13as_windows")
        except Exception:
            print('Nope')
        else:
            df.loc[:, column] = x13_result.trend
            #df[column] = x13_result.trend


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
    df_filtered = df.copy()
    
    for column_name in column_names:
        Q1 = df[column_name].quantile(0.25)
        Q3 = df[column_name].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        df_filtered = df_filtered[(df_filtered[column_name] >= lower_bound) & (df_filtered[column_name] <= upper_bound)]
    
    return df_filtered
    

df = pd.read_csv('data/2024_03_11.csv', index_col='fecha', parse_dates=True, date_format='%d/%m/%Y')

# Slice the DataFrame to get data from 2000 onwards
panel = df['2000':]

# Apply x13_arima_analysis to each series
stationarize_panel(panel, ['SP74663','SF4782'])
remove_outliers(panel, ['SP74663','SF4782'])