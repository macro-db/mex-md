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