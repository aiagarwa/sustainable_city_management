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
def shortest_longLatDistance(location, locationDict):
    distances = {}
    for item in locationDict:
        distances[item] = hs.haversine(location, locationDict[item])
    return(min(distances, key=distances.get))


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
    for item in tmp_result: # Getting the closest locations of each bike.
        item["Location"] = shortest_longLatDistance((item["Latitude"], item["Longitude"]),fetch_Location())
    locations = fetch_Location()


    for loc in locations.keys(): # Making dictionary for updation.
        loc_Density[loc] = 0 

    density_counter = Counter(item["Location"] for item in tmp_result) # Counting and updating the above declared dictionary.
    for (loc, count) in density_counter.items():
        loc_Density[loc] = count

    for loc in locations.keys(): # Building the result.
        result_response.append({"Location" : loc,
                                "Density" : loc_Density[loc],
                                "Latitude" : locations[loc][0], 
                                "Longitude" : locations[loc][1]})

    return(result_response)

