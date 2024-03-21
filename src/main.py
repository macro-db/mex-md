import pandas as pd

from extract import extract
from utils import read_yaml
from df_utils import order, save, stationarize_df, slice_df_from_date, remove_outliers, apply_transformations, set_date_index, filter_dates_with_day_01

if __name__ == "__main__":

    # Read yaml file containing the base url, and the series ID, transformation, and desired name in the df
    settings = read_yaml("src/settings.yaml")
    base_url = settings['base_url']
    series = [key for key in settings.keys() if key != 'base_url']

    df = (
        extract(base_url, series) # Extract the data from the data source API
        .pipe(order) # Order the rows by date
        .pipe(save) # Save raw csv
        .pipe(set_date_index) # Turn the date column into the index of the df
        .pipe(filter_dates_with_day_01)
        .pipe(slice_df_from_date, start_date='2000-01-01') # Get only data starting in 2000
        #.pipe(stationarize_df, ['SP74663', 'SF4782']) #Stationarize selected columns
        #.pipe(remove_outliers, ['SP74663', 'SF4782']) # Remove outliers
        #.pipe(apply_transformations) 
        .pipe(save, prefix='sliced_', index=True)
    )


'''
SP74663:
   transformation: 1
SF4782:
   transformation: 4
'''