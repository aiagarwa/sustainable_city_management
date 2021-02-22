import json
import collections
from collections import Counter
from datetime import datetime, timedelta
from .fetch_bikeapi import bikeapi
from .store_bikedata_to_database import fetch_bike_stands_location
from .store_processed_bikedata_to_db import *
# Below function is used for calling the graph values for bike usage on the basis of location.
def graphvalue_call_locationbased(days_historical = 5):
    if days_historical == 1 or days_historical == 0:
            return ({"ERROR" : "Assign days_historic parameter >= 2."})

    now_time = datetime.now()
    day_ahead_tmp = (now_time - timedelta(days=-1)).strftime("%Y-%m-%dT00:00:00Z")    
    day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")    
    resultDictionary = {}
    fetched_data = fetch_processed_data(days_historical)
    fetched_predicted = fetch_predicted_data(day_ahead_tmp)
    for loc in fetched_data:
        if loc["name"] != "ALL_LOCATIONS":
            tmpDict = {}
            for item2 in loc["data"]:
                day = item2["day"].strftime("%Y-%m-%d")
                tmpDict[day] = item2["in_use"]
            
            for item in fetched_predicted:
                if item["name"] == loc["name"]:
                    tmpDict[day_ahead] = item["data"]["in_use"]

            tmpDict = dict(collections.OrderedDict(sorted(tmpDict.items())))
            resultDictionary[loc["name"]] = {"TOTAL_STANDS" : loc["data"][0]["total_stands"], "IN_USE" : tmpDict}

    return resultDictionary

# Below function is used for calling the graph values for overall bike usage over a given timespan and predict value a day ahead.
def graphvalue_call_overall(days_historical = 5):
    if days_historical == 1 or days_historical == 0:
            return ({"ERROR" : "Assign days_historic parameter >= 2."})

    now_time = datetime.now()
    day_ahead_tmp = (now_time - timedelta(days=-1)).strftime("%Y-%m-%dT00:00:00Z")    
    day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")    
    resultDictionary = {}
    try:
        fetched_data = fetch_processed_data(days_historical)
        fetched_predicted = fetch_predicted_data(day_ahead_tmp)
        tmpDict = {}
        for item in fetched_data[-1]["data"]:
            day = item["day"].strftime("%Y-%m-%d")
            tmpDict[day] = item["in_use"]
        tmpDict[day_ahead] = fetched_predicted[-1]["data"]["in_use"]
        tmpDict = dict(collections.OrderedDict(sorted(tmpDict.items())))
        resultDictionary["ALL_LOCATIONS"] = {"TOTAL_STANDS" : fetched_data[-1]["data"][0]["total_stands"],
                                            "IN_USE" : tmpDict}
        return resultDictionary

    except:
        return ({"ERROR" : "Check overall location API."})