import json
import collections
from collections import Counter
from datetime import datetime, timedelta
from .fetch_bikeapi import bikeapi
from ..ML_models.bikes_usage_prediction import predict_bikes_usage
from .store_bikedata_to_database import fetch_bike_stands_location

def graphvalue_call_locationbased(days_historical = 5):
    if days_historical == 1 or days_historical == 0:
            return ({"ERROR" : "Assign days_historic parameter >= 2."})

    tmpDict = bikeapi(historical=True)
    resultDict = {}
    now_time = datetime.now()
    day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
    all_locations = fetch_bike_stands_location()
    for location in tmpDict:
        resultDict[location] = {"TOTAL_STANDS" : 0, "IN_USE" : {}}
    for i in range(days_historical):
        InputDict = bikeapi(historical=True, days_historical = i)
        for location in InputDict:
            resultDict[location]["TOTAL_STANDS"] = InputDict[location]["TOTAL_STANDS"]
            resultDict[location]["IN_USE"][InputDict[location]["DAY"]] = InputDict[location]["IN_USE"]
    for location in resultDict:
        in_use_arr = []
        for day in resultDict[location]["IN_USE"]:
            in_use_arr.append(resultDict[location]["IN_USE"][day])
        predictedVal = predict_bikes_usage(in_use_arr, previous_days_to_consider = days_historical - 1)
        resultDict[location]["IN_USE"][day_ahead] = predictedVal
        resultDict[location]["IN_USE"] = dict(collections.OrderedDict(sorted(resultDict[location]["IN_USE"].items())))
    return resultDict


def graphvalue_call_overall(days_historical = 5):
    if days_historical == 1 or days_historical == 0:
            return ({"ERROR" : "Assign days_historic parameter >= 2."})
    tmpDict = bikeapi(historical=True)
    resultDict = {}
    now_time = datetime.now()
    day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
    resultDict["ALL_LOCATIONS"] = {"TOTAL_STANDS" : 0, "IN_USE" : {}}
    in_use_arr = []
    for i in range(days_historical):
        InputDict = bikeapi(historical=True, days_historical = i)
        in_use_total = 0
        day = (now_time - timedelta(days=i)).strftime("%Y-%m-%d")
        for location in InputDict:
            resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"] = resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"] + InputDict[location]["TOTAL_STANDS"]
            in_use_total = in_use_total + InputDict[location]["IN_USE"]
        resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"] == resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"]//2
        resultDict["ALL_LOCATIONS"]["IN_USE"][day] = in_use_total
        in_use_arr.append(in_use_total)
    predictedVal = predict_bikes_usage(in_use_arr, previous_days_to_consider = days_historical - 1)
    resultDict["ALL_LOCATIONS"]["IN_USE"][day_ahead] = predictedVal
    resultDict["ALL_LOCATIONS"]["IN_USE"] = dict(collections.OrderedDict(sorted(resultDict["ALL_LOCATIONS"]["IN_USE"].items())))
    return resultDict