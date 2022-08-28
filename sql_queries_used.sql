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
SELECT city_name,latitude,
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

