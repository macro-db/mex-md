import pandas as pd
import logging

from datetime import date

from utils import data_from_series, read_yaml, remove_commas, remove_ne, is_last_month


def extract():
    # Create the log
    logging.basicConfig(filename=f"log/{date.today().strftime('%Y_%m_%d')}.log", filemode="w", level=logging.INFO)

    # Read yaml file containing the base url, and the series ID, transformation, and desired name in the df
    settings = read_yaml("src/settings.yaml")
    base_url = settings['base_url']
    series = settings['series']

    # Get the first series to create an initial df
    first_serie = series[0]
    df = pd.DataFrame(data_from_series(base_url, first_serie)['datos'])
    df.rename(columns={"dato": first_serie}, inplace=True)

    # Merge the rest of series into the df, joined by the date column
    for serie in series[1:]:
        try:
            temp_df = pd.DataFrame(data_from_series(base_url, serie)['datos'])

        except Exception:
            logging.error(f'Serie{serie} could not be retreived')
        
        else:
            temp_df.rename(columns={"dato": serie}, inplace=True)

            last_observation_date = temp_df['fecha'].iloc[-1]

            if not is_last_month(last_observation_date):
                logging.warning(f"Serie:{serie} seems to be outdated")
            
            df = df.merge(temp_df, on='fecha', how='outer')

    return df


def transform(df):
    """Transforms the raw dataset. If we want to provide both raw and balanced panels,
    maybe this step should be done later
    """

    df['fecha'] = pd.to_datetime(df['fecha'], dayfirst=True)
    df.sort_values(by=['fecha'], inplace=True)
    df['fecha'] = df['fecha'].dt.strftime('%d/%m/%Y')

    # Read the settings file to get the desired transformation for each series
    settings = read_yaml("src/settings.yaml")
    series = settings['series']

    for serie in series:
        # Turn the column to numeric, and apply its corresponding transformation
        # df[serie] = pd.to_numeric(df[serie])

        # Remove commas used as digit group separator
        try:
            df[serie] = df[serie].transform(remove_ne)
            df[serie] = df[serie].transform(remove_commas)
        except KeyError:
            pass
        
    return df


def load(df):
    today = date.today().strftime("%Y_%m_%d")
    df.to_csv(f'data/{today}.csv', index=False)


if __name__ == "__main__":
    # Extract the data from the data source API
    df = extract()
    # Transform the data given the desired transformations
    df = transform(df)
    # Load the output to a csv file
    load(df)

