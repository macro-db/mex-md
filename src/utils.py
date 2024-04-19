import datetime
import os
import random

import numpy as np
import pandas as pd
import requests
import yaml

API_KEY = [
    "deaba6cde13b994d8617049af1794580b35cd869725a78686877ea931ccb2d48",
    "abf532f9317fb2f09f9af67285987c8ca93aa63d40497110ba82fe05722a18d2",
]


def data_from_banxico(series):
    # Create session and add necessary headers
    session = requests.Session()
    headers = {"Bmx-Token": random.choice(API_KEY), "Accept": "application/json"}
    # Add desired series to request
    url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{series}/datos"
    response = session.get(url, headers=headers).json()
    # Return the response
    df = pd.DataFrame(response["bmx"]["series"][0]["datos"])
    df.rename(columns={"dato": series}, inplace=True)

    return df


INEGI_API_KEY = os.environ.get("INEGI_API_KEY")


def data_from_inegi(series):
    url = f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{series}/es/0700/false/BIE/2.0/{INEGI_API_KEY}?type=json"
    session = requests.Session()
    response = session.get(url).json()

    df = pd.DataFrame(response["Series"][0]["OBSERVATIONS"])[
        ["TIME_PERIOD", "OBS_VALUE"]
    ]

    # Convert TIME_PERIOD column to datetime
    df["TIME_PERIOD"] = pd.to_datetime(df["TIME_PERIOD"], format="%Y/%m")

    # Format datetime as 'DD/MM/YYYY'
    df["TIME_PERIOD"] = df["TIME_PERIOD"].dt.strftime("%d/%m/%Y")

    df = df.rename(columns={"TIME_PERIOD": "fecha", "OBS_VALUE": series})

    return df


def read_yaml(yaml_file):
    with open(yaml_file, "r") as file:
        data = yaml.safe_load(file)
    return data


def remove_commas(number):
    return str(number).replace(",", "")


def remove_ne(string):
    if pd.isna(string):
        return string
    else:
        return string.replace("N/E", "")


def is_last_month(date):
    date_month = date.split("/")[1]

    actual_date = datetime.date.today().replace(day=1)
    last_month = (actual_date - datetime.timedelta(days=1)).strftime("%m")

    return date_month == last_month

# Function to remove leading and trailing NaNs from a series
def remove_leading_trailing_nans(series):
    start_index = series.first_valid_index()
    end_index = series.last_valid_index()
    return series.loc[start_index:end_index]
