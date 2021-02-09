import requests
import json
from collections import Counter
from datetime import datetime, timedelta

# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).
def bikeAPI(historical = False, locations = False, minutes_delay = 5):    
    now_time = datetime.now()
    curr_time = now_time.strftime("%Y%m%d%H%M")
    url = ""
    if historical == True :
        delay_time =  (now_time - timedelta(days=1)).strftime("%Y%m%d%H%M")
        url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom="+str(delay_time)+"&dto="+str(curr_time) # Setting the Last Reading data URL to be called upon.
    else:
        delay_time =  (now_time - timedelta(minutes=minutes_delay)).strftime("%Y%m%d%H%M")
        url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom="+str(delay_time)+"&dto="+str(curr_time) # Setting the Last Reading data URL to be called upon.

    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    result_response = [] # Storing end result.
    tmp_result = json.loads(response.text)
    for item in tmp_result:
        for stand_details in item["historic"]:
            available_bike_stands = stand_details["available_bike_stands"]
            bike_stands = stand_details["bike_stands"]
            timestamp = stand_details["time"]
        if locations == True:
            result_response.append({"LOCATION" : item["name"],
                                    "LATITUDE" : item["latitude"], 
                                    "LONGITUDE" : item["longitude"]})
        else:    
            result_response.append({"LOCATION" : item["name"],
                                    "TOTAL_STANDS" : bike_stands,
                                    "IN_USE" : available_bike_stands,
                                    "TIME" : timestamp})

    print(len(result_response))
    return(result_response)