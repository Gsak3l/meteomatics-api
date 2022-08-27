from datetime import datetime, date, timedelta

import requests

import handle_data as hd

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
    # max 10 params for free api
    # parameters
    # min-max daily temp can be calculated without api call,
    # weather symbol doesn't seem necessary, it's just an icon
    params = [
        't_2m:C', 'wind_speed_10m:ms', 'wind_dir_10m:d', 'wind_gusts_10m_1h:ms',
        'wind_gusts_10m_24h:ms', 'msl_pressure:hPa', 'precip_1h:mm', 'precip_24h:mm'
    ]

    # locations
    locations = [
        '37.9,23.7',
        '52.5,13.4',
        '59.9,10.7'
    ]

    api_dct = {
        'base': f'https://{USERNAME}:{PASSWORD}@api.meteomatics.com',  # base url
        'valid_datetime': f'/{get_dates()}' + ':PT1H',  # PT1H = 1 hour
        'parameters': '/' + ','.join(params),  # looping through the params list
        'locations': '/' + '+'.join(locations),  # Athens, Berlin, Oslo
        'format': '/csv'  # format of the retrieved data
    }

    url = ''
    for key, value in api_dct.items():
        url += value

    print(url)

    data = requests.get(url).text
    return data


hd.clean_data(request_data())
