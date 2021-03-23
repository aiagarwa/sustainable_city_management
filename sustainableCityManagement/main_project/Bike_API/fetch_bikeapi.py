import sys
from .store_bikedata_to_database import StoreBikeDataToDatabase
from ..Logs.service_logs import bike_log
from ..Config.config_handler import read_config
import datetime
import copy
from collections import Counter
import collections
import json

# Calling logging function for bike _API
logger = bike_log()

# Calling Config values for processing api.
config_vals = read_config("Bike_API")
if config_vals is None:
    logger.error('No data retrieved from config files.')

# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).


class FetchBikeApi:
    def bikeapi(self, locations=False, store_bike_data_to_database = StoreBikeDataToDatabase()):
        now_time = datetime.datetime.now()
        tmp_result = []
        result_response = {}
        if locations == True:
            location_data = store_bike_data_to_database.fetch_bike_stands_location()
            for loc in location_data:
                result_response[loc["name"]] = {
                    "LATITUDE": loc["latitude"],
                    "LONGITUDE": loc["longitude"]
                }
            if result_response is None:
                logger.error('No location data was retrieved.')
            return(result_response)

        tmp_result = store_bike_data_to_database.fetch_data_from_db_for_minutes()

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
                "TOTAL_STANDS": bike_stands,
                "IN_USE": in_use_bikes,
                "TIME": now_time.strftime("%Y-%m-%d %H:%M")
            }
        if result_response is None:
            logger.error('No bike usage data was retrieved from DB.')
        return(result_response)
