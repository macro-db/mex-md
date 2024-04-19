import pandas as pd

from df_utils import (add_indicators, apply_transformations,
                      create_quarterly_data, fillna_with_zero,
                      filter_dates_with_day_01, order, remove_outliers, save,
                      set_date_index, slice_df_from_date, stationarize_df)
from extract import extract
from utils import read_yaml

if __name__ == "__main__":

    # Read yaml file containing the base url, and the series ID, transformation, and desired name in the df
    series = read_yaml("src/settings.yaml")

    df = (
        extract(series)  # Extract the data from the data source API
        .pipe(order)  # Order the rows by date
        #.pipe(save, index=True)  # Save raw csv
        .pipe(filter_dates_with_day_01)
        .pipe(slice_df_from_date, start_date="1985-01-01")  # Get only data starting in 1985
        .pipe(stationarize_df)
        .pipe(save, prefix="MD_", index=True)
        .pipe(create_quarterly_data)
        .pipe(add_indicators)
        .pipe(save, prefix="QD_", index=True)
    )