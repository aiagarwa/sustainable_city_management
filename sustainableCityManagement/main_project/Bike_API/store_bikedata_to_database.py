from mongoengine import *
import requests
import json
from datetime import datetime, timedelta
import pytz

# Connect to Database
connect('sustainableCityManagement', host='mongodb://127.0.0.1:27017/sustainableCityManagement')

# Define Embedded Document structure to store in Mongo DB. This contains Data related to Bikes availability. This is used by Bikestands Document
class BikeAvailability(EmbeddedDocument):
    bike_stands = IntField()
    available_bike_stands = IntField()
    time = DateTimeField()
    # time = StringField(max_length=200) #, unique=True)

# Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity 
class BikeStands(Document):
    historical = ListField(EmbeddedDocumentField(BikeAvailability))
    name = StringField(max_length=200)
    meta = {'collection': 'BikeUsage'}

# Define Document for location
class BikesStandsLocation(Document):
    name = StringField(max_length=200, required=True)
    latitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    longitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'BikeStandsLocation'}

def save_bike_stands_location():
    url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/stations"
    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    loc_result = json.loads(response.text)
    for item in loc_result:
        standLocations = BikesStandsLocation(name = item["st_NAME"], latitude = item["st_LATITUDE"], longitude = item["st_LONGITUDE"])
        standLocations.save()


# This method gets the data from API for a single day and store in DB.
def bikedata_day(days_historical):
    now_time = datetime.now(pytz.utc)
    curr_time = (now_time - timedelta(days=days_historical)).strftime("%Y%m%d%H%M") 
    delay_time =  (now_time - timedelta(days=days_historical + 1)).strftime("%Y%m%d%H%M")
    url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom="+str(delay_time)+"&dto="+str(curr_time)
    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    tmp_result = json.loads(response.text)
    for item in tmp_result:
        biketemp = BikeStands._get_collection().count_documents({ 'name': item["name"] }) # Get the number of documents with a particular location name
        if biketemp < 1 :
            bikestands = BikeStands(name = item["name"])
            bikestands.save()  # Saves Location details in MongoDB as a Document if it does not exist
        else:
            bikestands = BikeStands(name = item["name"])
        bikestands = bikestands._qs.filter(name = item["name"]).first()
        if bikestands is not None:
            for stand_details in item["historic"]:
                datetimeConvert = datetime.strptime(stand_details["time"], "%Y-%m-%dT%H:%M:%SZ")
                bikesAvailability = BikeAvailability(bike_stands = stand_details["bike_stands"], available_bike_stands = stand_details["available_bike_stands"], time = datetimeConvert)
                bikestands.historical.append(bikesAvailability)
            bikestands.save() # Saves Bike Availability Data
        else:
            print("Empty")

# This method gets the data from API every 5 minutes and store in DB.
def bikedata_minutes():
    now_time = datetime.now(pytz.utc)
    curr_time = now_time.strftime("%Y%m%d%H%M") 
    url = ""
    delay_time =  (now_time - timedelta(minutes=5)).strftime("%Y%m%d%H%M")
    url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom="+str(delay_time)+"&dto="+str(curr_time)
    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    tmp_result = json.loads(response.text)
    for item in tmp_result:
        biketemp = BikeStands._get_collection().count_documents({ 'name': item["name"] }) # Get the number of documents with a particular location name
        if biketemp < 1 :
            bikestands = BikeStands(name = item["name"])
            bikestands.save()  # Saves Location details in MongoDB as a Document if it does not exist
        else:
            bikestands = BikeStands(name = item["name"])
        bikestands = bikestands._qs.filter(name = item["name"]).first()
        if bikestands is not None:
            for stand_details in item["historic"]:
                # print(stand_details["time"])
                datetimeConvert = datetime.strptime(stand_details["time"], "%Y-%m-%dT%H:%M:%SZ")
                bikesAvailability = BikeAvailability(bike_stands = stand_details["bike_stands"], available_bike_stands = stand_details["available_bike_stands"], time = datetimeConvert)
                bikestands.historical.append(bikesAvailability)
            bikestands.save() # Saves Bike Availability Data
        else:
            print("Empty")

# This method stores the data for n number of days in MongoDB
def save_historic_data_in_db(days_historical):
    for i in range(days_historical):
        bikedata_day(i)

# Fetch Data for Locations
def fetch_bike_stands_location():
    q_set = BikesStandsLocation.objects() # Fetch Data from DB
    json_data = q_set.to_json() # Converts the Processed Bikes Data from DB into JSON format
    locations = json.loads(json_data)
    return locations

#Fetch bikedata from db for a particular date
def fetch_data_from_db_for_day(dateForData):
    start_date_str = dateForData.strftime("%Y-%m-%dT00:00:00Z")
    end_date_str = dateForData.strftime("%Y-%m-%dT23:59:59Z")
    start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%SZ")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%SZ")
    pipeline = [
    { "$project": {
        "historical": {"$filter": {
            "input": "$historical",
            "as": "historical",
            "cond": {"$and":[ 
                { "$lte": ["$$historical.time",end_date]},
                { "$gte": ["$$historical.time", start_date]}
            ]}
        }
        },
        "name":"$name",
        "_id":0} 
        },
    ]
    q_set = BikeStands.objects().aggregate(*pipeline)# Fetch Data from DB
    list_q_set = list(q_set)
    return list_q_set

# This method returns the Bikes availablity data for all locations (Bike Stands) for last few minutes
def fetch_data_from_db_for_minutes(minutes):
    now_time = datetime.now(pytz.utc)
    curr_time = now_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    curr_time_formatted = datetime.strptime(curr_time, "%Y-%m-%dT%H:%M:%SZ")
    delay_time = (now_time - timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")
    delay_time_formatted = datetime.strptime(delay_time, "%Y-%m-%dT%H:%M:%SZ")
    pipeline = [
    { "$project": {
        "historical": {"$filter": {
            "input": "$historical",
            "as": "historical",
            "cond": {"$and":[ 
                { "$lte": ["$$historical.time",curr_time_formatted]},
                { "$gte": ["$$historical.time", delay_time_formatted]}
            ]}
        }
        },
        "name":"$name",
        "_id":0} 
        },
    ]
    q_set = BikeStands.objects().aggregate(*pipeline)# Fetch Data from DB
    return list(q_set)

In = input("SAVE DATA IN DB ? :")
if In == "yes":
    save_historic_data_in_db(5)
    save_bike_stands_location()
else:
    pass
