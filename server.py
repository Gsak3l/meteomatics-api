# external python libraries
import uvicorn

from fastapi import FastAPI

# local python files
import database_related as dr
import handle_data as hd

app = FastAPI(debug=True)


# returns true if the api call is successful
@app.get('/status')
async def check_status():
    return {'status': 'ok'}


# list the latest forecast for each location for every day
@app.get('/day/last')
async def get_last_day():
    result = dr.select_latest_forecast()
    return hd.convert_timedelta_to_string(result)


# list the average the_temp of the last 3 forecasts for each location for every day
@app.get('/three_average')
async def get_three_average_day():
    return dr.select_three_average_forecast()


# get the top n locations based on each available metric where n is a parameter given to the API call.
@app.get('/top/{n}')
async def get_top_n(n: int):
    return hd.get_top_n_locations(n)


def run_server():
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=False)
