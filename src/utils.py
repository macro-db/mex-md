import datetime
import requests
import os
import yaml
import numpy as np

API_KEY = "deaba6cde13b994d8617049af1794580b35cd869725a78686877ea931ccb2d48"

def data_from_series(base_url, series, unique_series=True):
    # Create session and add necessary headers
    session = requests.Session()
    headers = {'Bmx-Token': API_KEY, 'Accept': 'application/json'}
    # Add desired series to request
    requested_data = base_url + series + '/datos'
    response = session.get(requested_data, headers=headers).json()
    # Return the response
    if unique_series:
        return response['bmx']['series'][0]
    return response


def read_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data


def remove_commas(number):
    return str(number).replace(',', '')


def remove_ne(number):
    return number.replace('N/E', np.nan)


def is_last_month(date):
    date_month = date.split('/')[1]

    actual_date = (datetime.date.today().replace(day=1))
    last_month = (actual_date - datetime.timedelta(days=1)).strftime('%m')

    return date_month == last_month


def transformation(tcode, x):
    n = len(x)
    small = 1e-10  # Define your small value here

    if tcode == 1:  # Level (no transformation)
        y = x

    elif tcode == 2:  # First difference
        y = np.diff(x, axis=0)

    elif tcode == 3:  # Second difference
        y = np.diff(x, n=2, axis=0)

    elif tcode == 4:  # Natural log
        y = np.where(np.min(x) < small, np.nan, np.log(x))

    elif tcode == 5:  # First difference of natural log
        if np.min(x) > small:
            y = np.diff(np.log(x), axis=0)
        else:
            y = np.full(n-1, np.nan)  # Output NaNs if condition is not met

    elif tcode == 6:  # Second difference of natural log
        if np.min(x) > small:
            y = np.diff(np.log(x), n=2, axis=0)
        else:
            y = np.full(n-2, np.nan)  # Output NaNs if condition is not met

    elif tcode == 7:  # First difference of percent change
        y1 = np.diff(x / x[:-1], axis=0)
        y = np.diff(y1, axis=0)

    else:
        raise ValueError("Invalid transformation code")

    return y
