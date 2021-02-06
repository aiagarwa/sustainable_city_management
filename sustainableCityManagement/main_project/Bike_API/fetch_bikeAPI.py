import requests
import json
import haversine as hs
from collections import Counter

# Function to fetch respective location names and latitude longitudes.
def fetch_Location():
    url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/stations" # Setting the URL for fetching the respective location names and latitude longitudes.  
    payload={} 
    headers = {}
    locations = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    response = json.loads(response.text)
    counter = 0
    for item in response:
        locations[item["st_NAME"]] = (item["st_LATITUDE"],item["st_LONGITUDE"])
    return(locations)

# Finding Bikestand location closest to given bike.
def shortest_LatLongDistance(location, locationDict):
    distances = {}
    for item in locationDict:
        distances[item] = hs.haversine(location, locationDict[item])
    # print(type(min(distances)))
    key_min = min(distances.keys(), key=(lambda k: distances[k]))
    min_distLocation = min(distances, key=distances.get)
    return(min_distLocation, distances[key_min])


# Function for fetching the data from the URL.
def bikeAPI(historical = False):    
    # if historical == True :
    #     url = "https://data.smartdublin.ie/mobybikes-api/historical/" # Setting the Historical data URL to be called upon.
    # else:
    #     url = "https://data.smartdublin.ie/mobybikes-api/last_reading/" # Setting the Last Reading data URL to be called upon.
    
    url = "https://data.smartdublin.ie/mobybikes-api/last_reading/" # Setting the Last Reading data URL to be called upon.
    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    
    loc_Density = {} # For Storing density of the location.
    result_response = [] # Storing end result.
    tmp_result = json.loads(response.text)
    locations = []
    tmp_loc = []
    counter_avail = 0
    for item in tmp_result: # Getting the closest locations of each bike.
        item["Location"], distance = shortest_LatLongDistance((item["Latitude"], item["Longitude"]),fetch_Location())
        if float(distance) <= 0.025:
            item["Availability"] = True
            counter_avail += 1
        else:
            item["Availability"] = False
    locations = fetch_Location()

    for loc in locations.keys(): # Making dictionary for updation.
        loc_Density[loc] = 0 

    density_counter = Counter(item["Location"] for item in tmp_result) # Counting and updating the above declared dictionary.
    for (loc, count) in density_counter.items():
        loc_Density[loc] = count

    for loc in locations.keys(): # Building the result.
        counter = 0 
        for item in tmp_result:
            if item["Location"] == loc:
                if item["Availability"] == True:
                    counter += 1
        result_response.append({"LOCATION" : loc,
                                "DENSITY" : loc_Density[loc],
                                "AVAILABLE" : counter,
                                "IN-USE" : (loc_Density[loc] - counter),
                                "LATITUDE" : locations[loc][0], 
                                "LONGITUDE" : locations[loc][1]})


    return(result_response)

# bikeAPI()
