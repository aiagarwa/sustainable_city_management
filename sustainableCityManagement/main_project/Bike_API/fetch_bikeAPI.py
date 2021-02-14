import json
import collections
from collections import Counter
import copy
from datetime import datetime, timedelta
from .store_bikedata_to_database import fetch_data_from_db_for_day
from .store_bikedata_to_database import fetch_data_from_db_for_minutes
from .store_bikedata_to_database import fetch_bike_stands_location
# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).
def bikeapi(historical = False, locations = False, minutes_delay = 5, days_historical = 0):    
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
    if historical == True :
        delay_time =  (now_time - timedelta(days=days_historical)).strftime("%Y%m%d%H%M")
        delay_time_formatted = datetime.strptime(delay_time,"%Y%m%d%H%M")
        tmp_result = fetch_data_from_db_for_day(delay_time_formatted)

# To be fixed.
    # else:
    #     tmp_result = fetch_Data_from_DB_for_minutes(minutes_delay) 

    counter = 0
    locations_arr = []
    for locations in tmp_result:
        if locations["name"] not in locations_arr :
            locations_arr.append(locations["name"])
    
    for location in locations_arr :
        in_use_bikes_arr = []
        for item in tmp_result:
            if location == item["name"]:
                in_use_bikes_arr.append(item["available_bike_stands"])
                bike_stands = item["bike_stands"]
                timestamp = delay_time
                in_use_bikes = sum(in_use_bikes_arr)//len(in_use_bikes_arr)
        
        result_response[location] = {
                                    "TOTAL_STANDS" : bike_stands,
                                    "IN_USE" : in_use_bikes,
                                    "DAY" : (now_time - timedelta(days=days_historical)).strftime("%Y-%m-%d")
                                    }
    return(result_response)
