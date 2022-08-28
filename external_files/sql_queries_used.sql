# ALL THE COMMANDS BELOW WERE USED FROM PYTHON USING THE mysql.connector MODULE

# Create a database with the name weather_db if this doesn't already exist
CREATE DATABASE IF NOT EXISTS weather_db;

# Create a table with the name weather_data if this doesn't already exist
CREATE TABLE IF NOT EXISTS weather_data
(
    id                      INT AUTO_INCREMENT PRIMARY KEY,
    city_name               VARCHAR(20),
    latitude                FLOAT,
    longitude               FLOAT,
    date                    DATE,
    time                    TIME,
    temperature_celsius     FLOAT,
    wind_speed_ms           FLOAT,
    wind_direction          INT,
    wind_gusts_ms_hourly    FLOAT,
    wind_gusts_ms_daily     FLOAT,
    pressure_hPa            FLOAT,
    precipitation_mm_hourly FLOAT,
    precipitation_mm_daily  FLOAT
);

# Insert data into the table, use the following syntax
INSERT INTO weather_data (city_name, latitude, longitude, date, time, temperature_celsius, wind_speed_ms,
                          wind_direction, wind_gusts_ms_hourly, wind_gusts_ms_daily, pressure_hPa,
                          precipitation_mm_hourly, precipitation_mm_daily)
VALUES ('London', 51.5074, 0.1278, '2020-01-01', '00:00:00', 5.0, 3.0, 180, 4.0, 5.0, 1010.0, 0.0, 0.0);

# List the latest forecast for each location for every day
SELECT w1.*
FROM weather_data AS w1
WHERE w1.time = (SELECT max(w2.time)
                 FROM weather_data AS w2
                 WHERE w1.date = w2.date)
ORDER BY w1.date;

# List the average the_temp of the last 3 forecasts for each location for every day
WITH TOP_THREE AS (SELECT *, ROW_NUMBER() over
(PARTITION BY city_name, date order by time DESC)
AS Row_Numb FROM weather_data)
SELECT city_name, date,
AVG(temperature_celsius) FROM TOP_THREE WHERE Row_Numb <= 3
GROUP BY city_name, date;

# List all the table fields
SELECT city_name,
       latitude,
       longitude,
       date,
       time,
       temperature_celsius,
       wind_speed_ms,
       wind_direction,
       wind_gusts_ms_hourly,
       wind_gusts_ms_daily,
       pressure_hPa,
       precipitation_mm_hourly,
       precipitation_mm_daily
FROM weather_data

