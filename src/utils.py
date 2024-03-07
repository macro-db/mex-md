import requests
import os
import yaml
import numpy as np

API_KEY = os.environ['API_KEY']

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
