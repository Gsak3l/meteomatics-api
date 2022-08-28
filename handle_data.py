# local python files
import pandas as pd
import database_related as dr


# column names for the dataframe, used in clean_api_data() and get_top_n_locations()
def get_column_names():
    column_names = ['city_name', 'latitude', 'longitude', 'date', 'time', 'temperature_celsius',
                    'wind_speed_ms', 'wind_direction', 'wind_gusts_ms_hourly', 'wind_gusts_ms_daily',
                    'pressure_hPa', 'precipitation_mm_hourly', 'precipitation_mm_daily']
    return column_names


# cleaning the names of the fields in the dataframe, creating a new city_name field, rearranging the columns
def clean_api_data(data):
    # saving data to a txt file
    with open('data.txt', 'w') as f:
        f.write(data)
    f.close()

    df = pd.read_csv('data.txt', sep=';', header=[0])

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

    # splitting datetime into date and time
    df['date'] = df['validdate'].str.split('T').str[0]
    df['time'] = df['validdate'].str.split('T').str[1].str.split('Z').str[0]

    # adding city name based on coordinates
    df.loc[df['latitude'] == 37.9, 'city_name'] = 'Athens'
    df.loc[df['latitude'] == 52.5, 'city_name'] = 'Berlin'
    df.loc[df['latitude'] == 59.9, 'city_name'] = 'Oslo'

    # rearranging columns
    df = df[get_column_names()]

    return df


# Get the top n locations based on each available metric where n is a parameter given to the API call.
def get_top_n_locations(n):
    dct = {}

    df = pd.DataFrame(dr.select_all(), columns=get_column_names())

    # converting timedelta64 to string, otherwise when returning the value it would show only seconds instead of hh:mm:ss
    df['time'] = df['time'].apply(
        lambda x: f'{x.components.hours:02d}:{x.components.minutes:02d}:{x.components.seconds:02d}'
    )

    for column_name in df.columns[5:]:
        df_col = df.sort_values(by=[column_name], ascending=False)
        dct[column_name] = df_col.head(n).to_dict('records')

    return dct


# converting timedelta64 to string, otherwise when returning the value it would show only seconds instead of hh:mm:ss
def convert_timedelta_to_string(df):
    df = pd.DataFrame(df).from_dict(df)
    df['time'] = df['time'].apply(
        lambda x: f'{x.components.hours:02d}:{x.components.minutes:02d}:{x.components.seconds:02d}'
    )
    return df.to_dict('records')
