import requests
import json
from collections import Counter
from datetime import datetime, timedelta

# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).
def bikeAPI(historical = False, delay = 5):    
    # if historical == True :
    #     url = "https://data.smartdublin.ie/mobybikes-api/historical/" # Setting the Historical data URL to be called upon.
    # else:
    #     url = "https://data.smartdublin.ie/mobybikes-api/last_reading/" # Setting the Last Reading data URL to be called upon.
    now_time = datetime.now()
    curr_time = now_time.strftime("%Y%m%d%H%M")
    delay_time =  (now_time - timedelta(minutes=delay)).strftime("%Y%m%d%H%M")
    url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom="+str(delay_time)+"&dto="+str(curr_time) # Setting the Last Reading data URL to be called upon.
    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    result_response = [] # Storing end result.
    tmp_result = json.loads(response.text)
    for item in tmp_result:
        for stand_details in item["historic"]:
            available_bike_stands = stand_details["available_bike_stands"]
            available_bikes = stand_details["available_bikes"]
        result_response.append({"LOCATION" : item["name"],
                        "AVAILABLE_STANDS" : available_bike_stands,
                        "AVAILABLE_BIKES" : available_bikes,
                        "LATITUDE" : item["latitude"], 
                        "LONGITUDE" : item["longitude"]})

    return(result_response)