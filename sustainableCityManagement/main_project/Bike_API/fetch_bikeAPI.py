import requests
import json
from collections import Counter
import copy
from datetime import datetime, timedelta

# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).
def bikeAPI(historical = False, locations = False, minutes_delay = 5, days_historical = 0):    
    now_time = datetime.now()
    curr_time = (now_time - timedelta(days=days_historical)).strftime("%Y%m%d%H%M") 
    url = ""
    if historical == True :
        delay_time =  (now_time - timedelta(days=days_historical + 1)).strftime("%Y%m%d%H%M")
        url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom="+str(delay_time)+"&dto="+str(curr_time) # Setting the Last Reading data URL to be called upon.
    else:
        delay_time =  (now_time - timedelta(minutes=minutes_delay)).strftime("%Y%m%d%H%M")
        url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom="+str(delay_time)+"&dto="+str(curr_time) # Setting the Last Reading data URL to be called upon.

    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    result_response = {} # Storing end result.
    tmp_result = json.loads(response.text)
    for item in tmp_result:
        for stand_details in item["historic"]:
            available_bike_stands = stand_details["available_bike_stands"]
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
                                    "IN_USE" : available_bike_stands,
                                    "TIME" : timestamp
                                    }

    return(result_response)

def graphVals(locationsBased = True, days_historical = 2):
    dataDict = bikeAPI(historical=True)
    tmpDict = copy.deepcopy(dataDict)
    now_time = datetime.now()
    curr_day = (now_time - timedelta(days=0)).strftime("%d-%m-%Y")
    for item in tmpDict:
        tmpDict[item]["TOTAL_STANDS"] = {curr_day : tmpDict[item]["TOTAL_STANDS"]}
        tmpDict[item]["IN_USE"] = {curr_day : tmpDict[item]["IN_USE"]}
    if locationsBased == True:
        if days_historical == 0:
            return(dataDict)
        Locations = list(dataDict.keys())
        if days_historical == 1:
            tmpCall = bikeAPI(historical=True, days_historical = 0)
            day = (now_time - timedelta(days=1)).strftime("%d-%m-%Y")
            for loc in tmpCall:
                # dataDict[loc]["TOTAL_STANDS"] = dataDict[loc]["TOTAL_STANDS"] + tmpCall[loc]["TOTAL_STANDS"]
                tmpDict[loc]["TOTAL_STANDS"] = tmpCall[loc]["TOTAL_STANDS"]
                dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"] + tmpCall[loc]["IN_USE"]
                tmpDict[loc]["IN_USE"][day] = tmpCall[loc]["IN_USE"]
        else:
            for i in range(1,days_historical):
                tmpCall = bikeAPI(historical=True, days_historical = i)
                day = (now_time - timedelta(days=i)).strftime("%d-%m-%Y")
                for loc in tmpCall:
                    tmpDict[loc]["TOTAL_STANDS"] = tmpCall[loc]["TOTAL_STANDS"]
                    dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"] + tmpCall[loc]["IN_USE"]
                    tmpDict[loc]["IN_USE"][day] = tmpCall[loc]["IN_USE"]
        for loc in dataDict:
            day_ahead = (now_time - timedelta(days=-1)).strftime("%d-%m-%Y")
            dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"]//days_historical
            tmpDict[loc]["IN_USE"][day_ahead] = dataDict[loc]["IN_USE"]
        return tmpDict

    if locationsBased == False:
        keyVal = "ALL_LOCATIONS"
        tmpDict = {keyVal : {"TOTAL_STANDS" : 0, "IN_USE" : {}}}
        if days_historical == 0:
            return(tmpDict)
        Locations = list(dataDict.keys())
        if days_historical == 1:
            tmpCall = bikeAPI(historical=True, days_historical = 0)
            day = (now_time - timedelta(days=1)).strftime("%d-%m-%Y")
            for loc in tmpCall:
                # dataDict[loc]["TOTAL_STANDS"] = dataDict[loc]["TOTAL_STANDS"] + tmpCall[loc]["TOTAL_STANDS"]
                tmpDict[keyVal]["TOTAL_STANDS"] = tmpDict[keyVal]["TOTAL_STANDS"] + tmpCall[loc]["TOTAL_STANDS"]
                dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"] + tmpCall[loc]["IN_USE"]
                tmpDict[loc]["IN_USE"][day] = tmpCall[loc]["IN_USE"]
        else:
            for i in range(days_historical):
                in_use_total = 0
                tmpCall = bikeAPI(historical=True, days_historical = i)
                day = (now_time - timedelta(days=i)).strftime("%d-%m-%Y")
                for loc in tmpCall:
                    tmpDict[keyVal]["TOTAL_STANDS"] = tmpDict[keyVal]["TOTAL_STANDS"] + tmpCall[loc]["TOTAL_STANDS"]
                    dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"] + tmpCall[loc]["IN_USE"]
                    in_use_total = in_use_total + tmpCall[loc]["IN_USE"]
                    tmpDict[keyVal]["IN_USE"][day] = in_use_total
        in_use_total = 0
        day_ahead = (now_time - timedelta(days=-1)).strftime("%d-%m-%Y")
        for item in dataDict:
            in_use_total = in_use_total + dataDict[item]["IN_USE"]
            day_ahead = (now_time - timedelta(days=-1)).strftime("%d-%m-%Y")
            dataDict[loc]["IN_USE"] = dataDict[loc]["IN_USE"]//days_historical
        tmpDict[keyVal]["IN_USE"][day_ahead] = in_use_total//days_historical
        tmpDict[keyVal]["TOTAL_STANDS"] = tmpDict[keyVal]["TOTAL_STANDS"]//days_historical
        return tmpDict
