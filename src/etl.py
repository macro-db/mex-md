import pandas as pd

from utils import data_from_series, read_yaml, remove_commas, remove_ne


def extract():
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

        temp_df = pd.DataFrame(data_from_series(base_url, serie)['datos'])
        temp_df.rename(columns={"dato": serie}, inplace=True)

        df = df.merge(temp_df, on='fecha', how='outer')

    return df


def transform(df):
    """Transforms the raw dataset. If we want to provide both raw and balanced panels,
    maybe this step should be done later
    """

    # Read the settings file to get the desired transformation for each series
    settings = read_yaml("src/settings.yaml")
    series = settings['series']

    for serie in series:
        # Turn the column to numeric, and apply its corresponding transformation
        # df[serie] = pd.to_numeric(df[serie])

        # Remove commas used as digit group separator
        df[serie] = df[serie].transform(remove_ne)
        df[serie] = df[serie].transform(remove_commas)

    return df


def load(df):
    df.to_csv('out_prueba.csv', index=False)


if __name__ == "__main__":
    # Extract the data from the data source API
    df = extract()
    # Transform the data given the desired transformations
    df = transform(df)
    # Load the output to a csv file
    load(df)

