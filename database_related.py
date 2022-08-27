import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="admin",
    passwd="admin",
    database="weather_db"
)
my_cursor = mydb.cursor()


# creates the database
def create_database():
    my_cursor.execute('CREATE DATABASE IF NOT EXISTS weather_db')
    mydb.commit()


# creates the table that will contain the weather data
def create_tables():
    my_cursor.execute('CREATE TABLE IF NOT EXISTS weather_data (id INT AUTO_INCREMENT PRIMARY KEY, '
                      'city_name VARCHAR(20),latitude FLOAT, longitude FLOAT, date DATE, time TIME, '
                      'temperature_celsius FLOAT, wind_speed_ms FLOAT, wind_direction INT, '
                      'wind_gusts_ms_hourly FLOAT, wind_gusts_ms_daily FLOAT, pressure_hPa FLOAT, '
                      'precipitation_mm_hourly FLOAT, precipitation_mm_daily FLOAT)')
    mydb.commit()


# inserts the data into the table
def insert_data(data):
    # deletes all values from the table since it will be updated, and we don't need values older than 7 days
    my_cursor.execute('DELETE FROM weather_data')

    # inserts the new values
    for index, row in data.iterrows():
        # basically INSERT INTO table (FIELDS) VALUES (VALUES)
        my_cursor.execute('INSERT INTO weather_data (city_name, latitude, longitude, date, time, temperature_celsius, '
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
def select_latest_forecast():
    my_cursor.execute(
        'SELECT w1.* FROM weather_data AS w1 WHERE w1.time = '
        '(SELECT max(w2.time) FROM weather_data AS w2 WHERE w1.date = w2.date) '
        'ORDER BY w1.date;'
    )
    result = my_cursor.fetchall()
    return result


# select the average the_temp of the last 3 forecasts for each location for every day
def select_three_average_forecast():
    my_cursor.execute(
        'WITH TOP_THREE AS (SELECT *, ROW_NUMBER() over '
        '(PARTITION BY city_name, date order by time DESC) '
        'AS Row_Numb FROM weather_data) SELECT city_name, date, '
        'AVG(temperature_celsius) FROM TOP_THREE WHERE Row_Numb <= 3 '
        'GROUP BY city_name, date;')

    result = my_cursor.fetchall()
    return result


def manage_db(data):
    create_database()
    create_tables()
    insert_data(data)
