
import requests
import json
import collections
from collections import Counter
import copy
from datetime import datetime, timedelta
from .fetch_bikeAPI import bikeAPI
from mongoengine import *
import pytz
from ..ML_models.bikesUsagePrediction import predictBikesUsageTest
# from bikesUsagePrediction import predictBikesUsageTest
from .store_bike import fetch_Bike_Stands_Location

# Connect to Database
connect('sustainableCityManagement', host='mongodb://127.0.0.1:27017/sustainableCityManagement')

# Define Document Structure to store processed bike data in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity 
class BikeDataForCharts(Document):
    date = StringField(unique=True)
    result = StringField()
    meta = {'collection': 'BikeChartData'}


def graphValue_Call1(days_historical = 5):

    if days_historical == 1 or days_historical == 0:
            return ({"ERROR" : "Assign days_historic parameter >= 2."})

    tmpDict = bikeAPI(historical=True)
    resultDict = {}
    now_time = datetime.now()
    day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
    all_locations = fetch_Bike_Stands_Location()
    for location in tmpDict:
        resultDict[location] = {"TOTAL_STANDS" : 0, "IN_USE" : {}}
    for i in range(days_historical):
        InputDict = bikeAPI(historical=True, days_historical = i)
        for location in InputDict:
            resultDict[location]["TOTAL_STANDS"] = InputDict[location]["TOTAL_STANDS"]
            resultDict[location]["IN_USE"][InputDict[location]["DAY"]] = InputDict[location]["IN_USE"]
    for location in resultDict:
        in_use_arr = []
        for day in resultDict[location]["IN_USE"]:
            in_use_arr.append(resultDict[location]["IN_USE"][day])
        predictedVal = predictBikesUsageTest(in_use_arr, previous_days_to_consider = days_historical - 1)
        resultDict[location]["IN_USE"][day_ahead] = predictedVal
        resultDict[location]["IN_USE"] = dict(collections.OrderedDict(sorted(resultDict[location]["IN_USE"].items())))
    return resultDict

def graphValue_Call2(days_historical = 5):

    if days_historical == 1 or days_historical == 0:
            return ({"ERROR" : "Assign days_historic parameter >= 2."})

    tmpDict = bikeAPI(historical=True)
    resultDict = {}
    now_time = datetime.now()
    day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
    resultDict["ALL_LOCATIONS"] = {"TOTAL_STANDS" : 0, "IN_USE" : {}}
    in_use_arr = []
    for i in range(days_historical):
        InputDict = bikeAPI(historical=True, days_historical = i)
        in_use_total = 0
        day = (now_time - timedelta(days=i)).strftime("%Y-%m-%d")
        for location in InputDict:
            resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"] = resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"] + InputDict[location]["TOTAL_STANDS"]
            in_use_total = in_use_total + InputDict[location]["IN_USE"]
        resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"] == resultDict["ALL_LOCATIONS"]["TOTAL_STANDS"]//2
        resultDict["ALL_LOCATIONS"]["IN_USE"][day] = in_use_total
        in_use_arr.append(in_use_total)
    print(">>>>>>>>>>>>>>>>>",in_use_arr)
    predictedVal = predictBikesUsageTest(in_use_arr, previous_days_to_consider = days_historical - 1)
    resultDict["ALL_LOCATIONS"]["IN_USE"][day_ahead] = predictedVal
    resultDict["ALL_LOCATIONS"]["IN_USE"] = dict(collections.OrderedDict(sorted(resultDict["ALL_LOCATIONS"]["IN_USE"].items())))
    print(resultDict)


# def save_Data_In_DB(locationsBased = True, days_historical = 2):
#     chartData = graphValue_Call(locationsBased, days_historical)
#     now_time = datetime.now(pytz.utc)
#     now_time_format = now_time.strftime("%Y-%m-%d")
#     bikeDataForCharts = BikeDataForCharts(date = now_time_format, result = chartData)
#     bikeDataForCharts.save()

# # This method fetch the processed and predicted data from DB per day and return as dictionary.
# def fetch_Data_From_DB(date):
#     q_set = BikeDataForCharts.objects() # Fetch Data from DB
#     q_set_filter = q_set.filter(date=date).only('result')
#     json_data = q_set_filter.to_json() # Converts the Processed Bikes Data from DB into JSON format
#     dicts = json.loads(json_data)
#     return dicts


# graphValue_Call2(days_historical = 2)