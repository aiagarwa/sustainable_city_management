import json
import collections
from collections import Counter
import copy
from datetime import datetime, timedelta
from .store_bikedata_to_database import fetch_data_from_db_for_day
from .store_bikedata_to_database import fetch_data_from_db_for_minutes
from .store_bikedata_to_database import fetch_bike_stands_location
from ..Config.config_handler import read_config

config_vals = read_config("Bike_API")

# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).
def bikeapi(locations = False, minutes_delay = config_vals["default_live_delay_minutes"]):
    now_time = datetime.now()
    tmp_result = []
    result_response = {}
    if locations == True:
        location_data = fetch_bike_stands_location()
        for loc in location_data:
            result_response[loc["name"]] = {
                            "LATITUDE" : loc["latitude"], 
                            "LONGITUDE" : loc["longitude"]
                            }
        return(result_response)

    tmp_result = fetch_data_from_db_for_minutes(minutes_delay) 

# Going through all the items in the fetched data from DB and storing the average of daily usage (Overall).
    for item in tmp_result:
        in_use_bikes_arr = []
        for stand_details in item["historical"]:
            in_use_bikes_arr.append(stand_details["available_bike_stands"])
            bike_stands = stand_details["bike_stands"]
            in_use_bikes = sum(in_use_bikes_arr)//len(in_use_bikes_arr)

# TOTAL_STANDS represents total number of stands at the location.
# IN_USE represents total number of bike in usage.
# DAY represents the date for which data is fetched.
        result_response[item["name"]] = {
                                "TOTAL_STANDS" : bike_stands,
                                "IN_USE" : in_use_bikes,
                                "TIME" : now_time.strftime("%Y-%m-%d %H:%M")
                                }

    return(result_response)
