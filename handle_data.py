import pandas as pd
import database_related as dr


def clean_data(data):
    # saving data to a txt file
    with open('data/data.txt', 'w') as f:
        f.write(data)
    f.close()

    df = pd.read_csv('data/data.txt', sep=';', header=[0])

    # renaming df fields
    df.rename(columns={
        'lat': 'latitude',
        'lon': 'longitude',
        't_2m:C': 'temperature_celsius',
        'wind_speed_10m:ms': 'wind_speed_ms',
        'wind_dir_10m:d': 'wind_direction',
        'wind_gusts_10m_1h:ms': 'wind_gusts_ms_hourly',
        'wind_gusts_10m_24h:ms': 'wind_gusts_ms_daily',
        'msl_pressure:hPa': 'pressure_hPa',
        'precip_1h:mm': 'precipitation_mm_hourly',
        'precip_24h:mm': 'precipitation_mm_daily'
    }, inplace=True)
    df['city_name'] = ''

    # split datetime into date and time
    df['date'] = df['validdate'].str.split('T').str[0]
    df['time'] = df['validdate'].str.split('T').str[1].str.split('Z').str[0]

    # add city name based on coordinates
    df.loc[df['latitude'] == 37.9, 'city_name'] = 'Athens'
    df.loc[df['latitude'] == 52.5, 'city_name'] = 'Berlin'
    df.loc[df['latitude'] == 59.9, 'city_name'] = 'Oslo'

    # drop unnecessary columns
    # df.drop(['validdate'], axis=1, inplace=True)

    # re-arrange columns
    df = df[['city_name', 'latitude', 'longitude', 'date', 'time', 'temperature_celsius',
             'wind_speed_ms', 'wind_direction', 'wind_gusts_ms_hourly', 'wind_gusts_ms_daily',
             'pressure_hPa', 'precipitation_mm_hourly', 'precipitation_mm_daily']]

    dr.manage_db(df)
