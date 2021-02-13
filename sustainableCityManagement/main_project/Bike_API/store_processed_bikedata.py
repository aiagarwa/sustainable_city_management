import requests
import json
import collections
from collections import Counter
import copy
from datetime import datetime, timedelta
from .fetch_bikeAPI import bikeAPI
from mongoengine import *
import pytz

# Connect to Database
connect('sustainableCityManagement', host='mongodb://127.0.0.1:27017/sustainableCityManagement')


# Define Document Structure to store processed bike data in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity 
class BikeDataForCharts(Document):
    date = StringField(unique=True)
    result = StringField()
    meta = {'collection': 'BikeChartData'}

def graphVals(locationsBased = True, days_historical = 2):
    dataDict = bikeAPI(historical=True)
    tmpDict = copy.deepcopy(dataDict)
    now_time = datetime.now()
    curr_day = (now_time - timedelta(days=0)).strftime("%Y-%m-%d")
    for item in tmpDict:
        tmpDict[item]["TOTAL_STANDS"] = {curr_day : tmpDict[item]["TOTAL_STANDS"]}
        tmpDict[item]["IN_USE"] = {curr_day : tmpDict[item]["IN_USE"]}
    if locationsBased == True:
        if days_historical == 0:
            return(dataDict)
        Locations = list(dataDict.keys())
        if days_historical == 1:
            tmpCall = bikeAPI(historical=True, days_historical = 0)
            day = (now_time - timedelta(days=1)).strftime("%Y-%m-%d")
            for loc in tmpCall:
                tmpDict[loc]["TOTAL_STANDS"] = tmpCall[loc]["TOTAL_STANDS"]
                dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"] + tmpCall[loc]["IN_USE"]
                tmpDict[loc]["IN_USE"][day] = tmpCall[loc]["IN_USE"]
        else:
            for i in range(1,days_historical):
                tmpCall = bikeAPI(historical=True, days_historical = i)
                day = (now_time - timedelta(days=i)).strftime("%Y-%m-%d")
                for loc in tmpCall:
                    tmpDict[loc]["TOTAL_STANDS"] = tmpCall[loc]["TOTAL_STANDS"]
                    dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"] + tmpCall[loc]["IN_USE"]
                    tmpDict[loc]["IN_USE"][day] = tmpCall[loc]["IN_USE"]
        for loc in dataDict:
            day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
            dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"]//days_historical
            tmpDict[loc]["IN_USE"][day_ahead] = dataDict[loc]["IN_USE"]
            tmpDict[loc]["IN_USE"] = collections.OrderedDict(sorted(tmpDict[loc]["IN_USE"].items()))
        return tmpDict

    if locationsBased == False:
        keyVal = "ALL_LOCATIONS"
        tmpDict = {keyVal : {"TOTAL_STANDS" : 0, "IN_USE" : {}}}
        if days_historical == 0:
            return(tmpDict)
        Locations = list(dataDict.keys())
        if days_historical == 1:
            tmpCall = bikeAPI(historical=True, days_historical = 0)
            day = (now_time - timedelta(days=1)).strftime("%Y-%m-%d")
            for loc in tmpCall:
                tmpDict[keyVal]["TOTAL_STANDS"] = tmpDict[keyVal]["TOTAL_STANDS"] + tmpCall[loc]["TOTAL_STANDS"]
                dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"] + tmpCall[loc]["IN_USE"]
                tmpDict[loc]["IN_USE"][day] = tmpCall[loc]["IN_USE"]
        else:
            for i in range(days_historical):
                in_use_total = 0
                tmpCall = bikeAPI(historical=True, days_historical = i)
                day = (now_time - timedelta(days=i)).strftime("%Y-%m-%d")
                for loc in tmpCall:
                    tmpDict[keyVal]["TOTAL_STANDS"] = tmpDict[keyVal]["TOTAL_STANDS"] + tmpCall[loc]["TOTAL_STANDS"]
                    dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"] + tmpCall[loc]["IN_USE"]
                    in_use_total = in_use_total + tmpCall[loc]["IN_USE"]
                    tmpDict[keyVal]["IN_USE"][day] = in_use_total
        in_use_total = 0
        day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
        for item in dataDict:
            in_use_total = in_use_total + dataDict[item]["IN_USE"]
            day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
            dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"]//days_historical
        tmpDict[keyVal]["IN_USE"][day_ahead] = in_use_total//days_historical
        tmpDict[keyVal]["TOTAL_STANDS"] = tmpDict[keyVal]["TOTAL_STANDS"]//days_historical
        tmpDict[keyVal]["IN_USE"] = collections.OrderedDict(sorted(tmpDict[keyVal]["IN_USE"].items()))

        return tmpDict

# This method gets the processed and predicted data and store in DB.
def save_Data_In_DB(chartData):
    now_time = datetime.now(pytz.utc)
    now_time_format = now_time.strftime("%Y-%m-%d")
    bikeDataForCharts = BikeDataForCharts(date = now_time_format, result = chartData)
    bikeDataForCharts.save()

# This method fetch the processed and predicted data from DB per day and return as dictionary.
def fetch_Data_From_DB(date):
    q_set = BikeDataForCharts.objects() # Fetch Data from DB
    q_set_filter = q_set.filter(date=date).only('result')
    json_data = q_set_filter.to_json() # Converts the Processed Bikes Data from DB into JSON format
    dicts = json.loads(json_data)
    return dicts

# tmp = graphVals(True,2)
# result = json.dumps(tmp)
# save_Data_In_DB(result)

# fetch_Data_From_DB("2021-02-13")
