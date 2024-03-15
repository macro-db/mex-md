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
    """
    Stationarize the specified series in the DataFrame using X13-ARIMA analysis.

    Parameters:
        df (DataFrame): Input DataFrame.
        series (list): List of column names to stationarize.

    Returns:
        None
    """
    # Apply x13_arima_analysis to each series
    for column in series:
        try:
            # Perform X13-ARIMA analysis
            x13_result = sm.tsa.x13_arima_analysis(df[column], x12path="x13as")
        except Exception as e:
            print(f'Error on X13-ARIMA with series {column}: ', e)
        else:
            # Replace the original series with the trend component
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
    

