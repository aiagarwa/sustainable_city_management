import json
import collections
from collections import Counter
from datetime import datetime, timedelta
from .fetch_bikeapi import bikeapi
from ..ML_models.bikes_usage_prediction import predict_bikes_usage
from .store_bikedata_to_database import fetch_bike_stands_location

# Below function is used for calling the graph values for bike usage on the basis of location.
def graphvalue_call_locationbased(days_historical = 5):
    if days_historical == 1 or days_historical == 0:
            return ({"ERROR" : "Assign days_historic parameter >= 2."})

# Building base temporary dictionary with required fields.
    tmpDict = bikeapi(historical=True)

# Empty dictionary for storing our result.
    resultDict = {}
    now_time = datetime.now()
    day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
    # all_locations = fetch_bike_stands_location()

# Looping through all the locations in the fetched temporay dictionary and building base required dictionary structure.
    for location in tmpDict:
        resultDict[location] = {"TOTAL_STANDS" : 0, "IN_USE" : {}}

# Looping through the number of days we want historical data from and calling API with respective day as parameter.
    for i in range(days_historical):
        InputDict = bikeapi(historical=True, days_historical = i)
        for location in InputDict:
            resultDict[location]["TOTAL_STANDS"] = InputDict[location]["TOTAL_STANDS"]
            resultDict[location]["IN_USE"][InputDict[location]["DAY"]] = InputDict[location]["IN_USE"]

# Looping through all locations in resultDict and updating the TOTAL_STANDS and storing the respective date and IN_USE value for the date.
    for location in resultDict:
        in_use_arr = []
        for day in resultDict[location]["IN_USE"]:
            in_use_arr.append(resultDict[location]["IN_USE"][day])

# Calling the ML model for predicting the data for a day ahead.
        predictedVal = predict_bikes_usage(in_use_arr, previous_days_to_consider = days_historical - 1)
        resultDict[location]["IN_USE"][day_ahead] = predictedVal
        resultDict[location]["IN_USE"] = dict(collections.OrderedDict(sorted(resultDict[location]["IN_USE"].items())))
    return resultDict

# Below function is used for calling the graph values for overall bike usage over a given timespan and predict value a day ahead.
def graphvalue_call_overall(days_historical = 5):
    if days_historical == 1 or days_historical == 0:
            return ({"ERROR" : "Assign days_historic parameter >= 2."})

# Building base temporary dictionary with required fields.            
    tmpDict = bikeapi(historical=True)

# Empty dictionary for storing our result.
    resultDict = {}
    now_time = datetime.now()
    day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")

# Building base required dictionary structure.
    resultDict["ALL_LOCATIONS"] = {"TOTAL_STANDS" : 0, "IN_USE" : {}}
    in_use_arr = []

# Looping through the number of days we want historical data from and calling API with respective day as parameter.
    for i in range(days_historical):
        InputDict = bikeapi(historical=True, days_historical = i)
        in_use_total = 0
        day = (now_time - timedelta(days=i)).strftime("%Y-%m-%d")

# Looping through all locations in resultDict and storing the TOTAL_STANDS sum as well as the respective date and sum of IN_USE values for the date.
        for location in InputDict:
            resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"] = resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"] + InputDict[location]["TOTAL_STANDS"]
            in_use_total = in_use_total + InputDict[location]["IN_USE"]

# Dividing the TOTAL_STANDS value by 2, since values are repeated while recursive addtition above.
        resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"] == resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"]//2
        resultDict["ALL_LOCATIONS"]["IN_USE"][day] = in_use_total
        in_use_arr.append(in_use_total)

# Calling the ML model for predicting the data for a day ahead.
    predictedVal = predict_bikes_usage(in_use_arr, previous_days_to_consider = days_historical - 1)
    resultDict["ALL_LOCATIONS"]["IN_USE"][day_ahead] = predictedVal
    resultDict["ALL_LOCATIONS"]["IN_USE"] = dict(collections.OrderedDict(sorted(resultDict["ALL_LOCATIONS"]["IN_USE"].items())))
    return resultDict
