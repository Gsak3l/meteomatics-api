from datetime import datetime, date, timedelta
import json

import requests
import pandas as pd

# API CREDENTIALS
USERNAME = ''
PASSWORD = ''


# CONVERTING DATE RANGE TO ISO 8601 FORMAT
def get_dates():
    # today's date and 7 days from now
    today = datetime.now()
    one_week = datetime.now() + timedelta(days=7)

    # the format the api expects
    today = today.isoformat('T')
    one_week = one_week.isoformat('T')

    return f'{today}Z--{one_week}Z'


def request_data():
    api_dct = {
        'base': f'https://{USERNAME}:{PASSWORD}@api.meteomatics.com',
        'valid_datetime': f'/{get_dates()}' + ':PT1H', # PT1H = 1 hour
        'parameters': '/t_2m:C',
        'locations': '/37.9,23.7+52.5,13.4+59.9,10.7',  # Athens, Berlin, Oslo
        'format': '/json'
    }

    url = ''
    for key, value in api_dct.items():
        url += value

    print(url)

    data = requests.get(url).json()['data']
    print(json.dumps(data, indent=4))


request_data()
