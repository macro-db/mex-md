import pandas as pd
from extract import extract
from df_utils import order, load
from df_transformations import stationarize_panel, slice_df_from_date, remove_outliers

if __name__ == "__main__":
    # Extract the data from the data source API
    df = extract()
    
    # Order the data by date
    df = order(df)
    
    # Load the raw output to a csv file
    load(df)

    # Convert 'fecha' column to datetime and set it as index
    df['fecha'] = pd.to_datetime(df['fecha'], format='%d/%m/%Y')
    df.set_index('fecha', inplace=True)

    # Slice the DataFrame to get data from 2000 onwards
    df = slice_df_from_date(df, start_date='2000-01-01')

    # Apply x13_arima_analysis to each series
    stationarize_panel(df, ['SP74663', 'SF4782'])
    
    # Remove outliers
    df = remove_outliers(df, ['SP74663', 'SF4782'])
    
    # Load balanced data to a csv file with index
    load(df, prefix='balanced_', index=True)