# external libraries
import mysql.connector

USERNAME = ''
PASSWORD = ''
DATABASE_NAME = 'weather_db'


# creates the database
def create_database():
    mydb = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        passwd=PASSWORD,
    )
    cursor = mydb.cursor()

    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}')
    mydb.commit()
    mydb.close()


# creates the table that will contain the weather data
def create_tables():
    mydb = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        passwd=PASSWORD,
        database=DATABASE_NAME
    )
    cursor = mydb.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS weather_data (id INT AUTO_INCREMENT PRIMARY KEY, '
                   'city_name VARCHAR(20),latitude FLOAT, longitude FLOAT, date DATE, time TIME, '
                   'temperature_celsius FLOAT, wind_speed_ms FLOAT, wind_direction INT, '
                   'wind_gusts_ms_hourly FLOAT, wind_gusts_ms_daily FLOAT, pressure_hPa FLOAT, '
                   'precipitation_mm_hourly FLOAT, precipitation_mm_daily FLOAT)')
    mydb.commit()
    mydb.close()


# inserts the data into the table
def insert_data(data):
    mydb = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        passwd=PASSWORD,
        database=DATABASE_NAME
    )
    cursor = mydb.cursor()
    # deletes all values from the table since it will be updated, and we don't need values older than 7 days
    cursor.execute('DELETE FROM weather_data')

    # inserts the new values
    for index, row in data.iterrows():
        # INSERT INTO table (FIELDS) VALUES (VALUES)
        cursor.execute('INSERT INTO weather_data (city_name, latitude, longitude, date, time, temperature_celsius, '
                       'wind_speed_ms, wind_direction, wind_gusts_ms_hourly, wind_gusts_ms_daily, '
                       'pressure_hPa, precipitation_mm_hourly, precipitation_mm_daily) '
                       'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                       (row['city_name'], row['latitude'], row['longitude'], row['date'], row['time'],
                        row['temperature_celsius'], row['wind_speed_ms'], row['wind_direction'],
                        row['wind_gusts_ms_hourly'], row['wind_gusts_ms_daily'], row['pressure_hPa'],
                        row['precipitation_mm_hourly'], row['precipitation_mm_daily']))
    mydb.commit()
    mydb.close()


# select the latest forecast for each location for every day
def select_latest_forecast(flag=False):
    mydb = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        passwd=PASSWORD,
        database=DATABASE_NAME
    )
    cursor = mydb.cursor()
    cursor.execute(
        'SELECT w1.* FROM weather_data AS w1 WHERE w1.time = '
        '(SELECT max(w2.time) FROM weather_data AS w2 WHERE w1.date = w2.date) '
        'ORDER BY w1.date;'
    )

    result = [dict((cursor.description[i][0], value) \
                   for i, value in enumerate(row)) for row in cursor.fetchall()]

    mydb.close()
    return (result[0] if result else None) if flag else result


# select the average the_temp of the last 3 forecasts for each location for every day
def select_three_average_forecast(flag=False):
    mydb = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        passwd=PASSWORD,
        database=DATABASE_NAME
    )
    cursor = mydb.cursor()

    cursor.execute(
        'WITH TOP_THREE AS (SELECT *, ROW_NUMBER() over '
        '(PARTITION BY city_name, date order by time DESC) '
        'AS Row_Numb FROM weather_data) SELECT city_name, date, '
        'AVG(temperature_celsius) FROM TOP_THREE WHERE Row_Numb <= 3 '
        'GROUP BY city_name, date;')

    # converts the db result into a dictionary that has both keys and values
    result = [dict((cursor.description[i][0], value) \
                   for i, value in enumerate(row)) for row in cursor.fetchall()]

    mydb.close()
    return (result[0] if result else None) if flag else result


# Get the top n locations based on each available metric where n is a parameter given to the API call.
def select_all():
    mydb = mysql.connector.connect(
        host="localhost",
        user=USERNAME,
        passwd=PASSWORD,
        database=DATABASE_NAME
    )
    cursor = mydb.cursor()

    cursor.execute('SELECT city_name, latitude, longitude, date, time, '
                   'temperature_celsius, wind_speed_ms, wind_direction, '
                   'wind_gusts_ms_hourly, wind_gusts_ms_daily, pressure_hPa, '
                   'precipitation_mm_hourly, precipitation_mm_daily FROM weather_data;')
    result = cursor.fetchall()

    mydb.close()
    return result


def manage_db(data):
    create_database()
    create_tables()
    insert_data(data)
