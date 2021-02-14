import requests
import json
import collections
from collections import Counter
import copy
from datetime import datetime, timedelta
from .store_bike import fetch_Data_from_DB_for_day, fetch_Data_from_DB_for_minutes, fetch_Bike_Stands_Location

# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).
def bikeAPI(historical = False, locations = False, minutes_delay = 5, days_historical = 0):    
    now_time = datetime.now()
    tmp_result = []
    result_response = {}
    if locations == True:
        location_data = fetch_Bike_Stands_Location()
        for loc in location_data:
            result_response[loc["name"]] = {
                            "LATITUDE" : loc["latitude"], 
                            "LONGITUDE" : loc["longitude"]
                            }
        return(result_response)

    if historical == True :
        delay_time =  (now_time - timedelta(days=days_historical)).strftime("%Y%m%d%H%M")
        delay_time_formatted = datetime.strptime(delay_time,"%Y%m%d%H%M")
        tmp_result = fetch_Data_from_DB_for_day(delay_time_formatted)
        # print(tmp_result)
    else:
        tmp_result = fetch_Data_from_DB_for_minutes(minutes_delay)

    for item in tmp_result:
        in_use_bikes_arr = []
        for stand_details in item["historical"]:
            in_use_bikes_arr.append(stand_details["available_bike_stands"])
            bike_stands = stand_details["bike_stands"]
            timestamp = delay_time
            in_use_bikes = sum(in_use_bikes_arr)//len(in_use_bikes_arr)
        result_response[item["name"]] = {
                                "TOTAL_STANDS" : bike_stands,
                                "IN_USE" : in_use_bikes,
                                "DAY" : (now_time - timedelta(days=days_historical)).strftime("%Y-%m-%d")
                                }
    # print(result_response)
    return(result_response)

# bikeAPI(historical = True)