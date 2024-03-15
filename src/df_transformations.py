import statsmodels.api as sm

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


def stationarize_panel(df, series):
    # Apply x13_arima_analysis to each series
    for column in series:
        try:
            x13_result = sm.tsa.x13_arima_analysis(df[column], x12path = "x13as")
        except Exception as e:
            print(f'Error on X13-ARIMA with series {column}: ', e)
        else:
            df.loc[:, column] = x13_result.trend


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
    

