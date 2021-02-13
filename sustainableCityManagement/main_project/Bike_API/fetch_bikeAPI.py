import requests
import json
import collections
from collections import Counter
import copy
from datetime import datetime, timedelta
from .store_bike import fetch_Data_from_DB_for_day, fetch_Data_from_DB_for_minutes

# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).
def bikeAPI(historical = False, locations = False, minutes_delay = 5, days_historical = 0):    
    now_time = datetime.now()
    curr_time = (now_time - timedelta(days=days_historical)).strftime("%Y%m%d%H%M") 
    tmp_result = []
    if historical == True :
        delay_time =  (now_time - timedelta(days=days_historical + 1)).strftime("%Y%m%d%H%M")
        delay_time_formatted = datetime.strptime(delay_time,"%Y%m%d%H%M")
        tmp_result = fetch_Data_from_DB_for_day(delay_time_formatted)
    else:
        tmp_result = fetch_Data_from_DB_for_minutes(minutes_delay)
    result_response = {} # Storing end result.
    for item in tmp_result:
        for stand_details in item["historical"]:
            in_use_bikes = stand_details["available_bike_stands"]
            bike_stands = stand_details["bike_stands"]
            timestamp = stand_details["time"]
        if locations == True:
            result_response[item["name"]] = {
                                    "LATITUDE" : item["latitude"], 
                                    "LONGITUDE" : item["longitude"]
                                        }
        else:    
            result_response[item["name"]] = {
                                    "TOTAL_STANDS" : bike_stands,
                                    "IN_USE" : in_use_bikes,
                                    "TIME" : timestamp
                                    }

    return(result_response)