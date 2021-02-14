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
    time = StringField(max_length=200) #, unique=True)

# Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity 
class BikeStands(Document):
    address = StringField(max_length=200, required=True)
    historical = ListField(EmbeddedDocumentField(BikeAvailability))
    latitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    longitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    name = StringField(max_length=200)
    meta = {'collection': 'BikeUsage'}

# Define Document for location
class BikesStandsLocation(Document):
    name = StringField(max_length=200, required=True)
    latitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    longitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'BikeStandsLocation'}

def save_Bike_Stands_Location():
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
    url = ""
    delay_time =  (now_time - timedelta(days=days_historical + 1)).strftime("%Y%m%d%H%M")
    url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom="+str(delay_time)+"&dto="+str(curr_time)
    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    tmp_result = json.loads(response.text)
    for item in tmp_result:
        biketemp = BikeStands._get_collection().count_documents({ 'name': item["name"] }) # Get the number of documents with a particular location name
        if biketemp < 1 :
            bikestands = BikeStands(name = item["name"], address = item["address"], latitude = item["latitude"], longitude = item["longitude"])
            bikestands.save()  # Saves Location details in MongoDB as a Document if it does not exist
        else:
            bikestands = BikeStands(name = item["name"], address = item["address"], latitude = item["latitude"], longitude = item["longitude"])
        bikestands = bikestands._qs.filter(name = item["name"]).first()
        if bikestands is not None:
            for stand_details in item["historic"]:
                bikesAvailability = BikeAvailability(bike_stands = stand_details["bike_stands"], available_bike_stands = stand_details["available_bike_stands"], time = stand_details["time"])
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
    # url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom=202102120810&dto=202102120815"
    # print(url)
    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    tmp_result = json.loads(response.text)
    # print(response)
    for item in tmp_result:
        biketemp = BikeStands._get_collection().count_documents({ 'name': item["name"] }) # Get the number of documents with a particular location name
        if biketemp < 1 :
            bikestands = BikeStands(name = item["name"], address = item["address"], latitude = item["latitude"], longitude = item["longitude"])
            bikestands.save()  # Saves Location details in MongoDB as a Document if it does not exist
        else:
            bikestands = BikeStands(name = item["name"], address = item["address"], latitude = item["latitude"], longitude = item["longitude"])
        bikestands = bikestands._qs.filter(name = item["name"]).first()
        if bikestands is not None:
            for stand_details in item["historic"]:
                # print(stand_details["time"])
                bikesAvailability = BikeAvailability(bike_stands = stand_details["bike_stands"], available_bike_stands = stand_details["available_bike_stands"], time = stand_details["time"])
                bikestands.historical.append(bikesAvailability)
            bikestands.save() # Saves Bike Availability Data
        else:
            print("Empty")

# This method stores the data for n number of days in MongoDB
def save_historic_data_in_DB(days_historical):
    for i in range(days_historical):
        bikedata_day(i)

# Fetch Data for Locations
def fetch_Bike_Stands_Location():
    q_set = BikesStandsLocation.objects() # Fetch Data from DB
    json_data = q_set.to_json() # Converts the Processed Bikes Data from DB into JSON format
    locations = json.loads(json_data)
    return locations

# This method returns the Bikes availablity data for all locations (Bike Stands) for a particular day
# def fetch_Data_from_DB_for_day(dateForData):
#     q_set = BikeStands.objects() # Fetch Data from DB
#     json_data = q_set.to_json() # Converts the Bikes Data from DB into JSON format
#     dicts = json.loads(json_data)
#     result_data = {}
#     list_result_data = []
#     for item in dicts:
#             result_data = {"historical":[]}
#             result_data["name"] = item["name"]
#             result_data["address"] = item["address"]
#             result_data["latitude"] = item["latitude"]
#             result_data["longitude"] = item["longitude"]
#             for details in item["historical"]:
#                 datetime_object = datetime.strptime(details["time"], "%Y-%m-%dT%H:%M:%SZ")
#                 temp_historical = {}
#                 if (datetime_object.year == dateForData.year and  datetime_object.month == dateForData.month and datetime_object.day == dateForData.day):
#                     datetimeNewFormat = datetime_object.strftime("%d%m%Y%H%M")
#                     temp_historical = {
#                                         "available_bike_stands" : details["available_bike_stands"], 
#                                         "bike_stands" : details["bike_stands"],
#                                         "time" : datetimeNewFormat
#                                             }
#                     result_data["historical"].append(temp_historical)
#             list_result_data.append(result_data)

#     return list_result_data


def fetch_Data_from_DB_for_day(dateForData):
    start_date_str = dateForData.strftime("%Y-%m-%dT")
    pipeline = [
    { "$unwind": "$historical" },
    { "$match": {"historical.time": {"$regex": "^"+start_date_str} } },
    { "$project": {"name":"$name","bike_stands":"$historical.bike_stands","available_bike_stands":"$historical.available_bike_stands","time":"$historical.time", "_id":0} },
    ]
    q_set = BikeStands.objects().aggregate(*pipeline)# Fetch Data from DB
    return list(q_set)





# This method returns the Bikes availablity data for all locations (Bike Stands) for last few minutes
def fetch_Data_from_DB_for_minutes(minutes):
    q_set = BikeStands.objects() # Fetch Data from DB
    json_data = q_set.to_json() # Converts the Bikes Data from DB into JSON format
    dicts = json.loads(json_data)
    now_time = datetime.now(pytz.utc)
    curr_time = now_time.strftime("%Y%m%d%H%M")
    curr_time_formatted = datetime.strptime(curr_time,"%Y%m%d%H%M")
    # print(curr_time_formatted)
    delay_time = (now_time - timedelta(minutes=minutes)).strftime("%Y%m%d%H%M")
    delay_time_formatted = datetime.strptime(delay_time,"%Y%m%d%H%M")
    # print (delay_time_formatted)
    result_data = {}
    list_result_data = []
    for item in dicts:
            result_data = {"historical":[]}
            result_data["name"] = item["name"]
            result_data["address"] = item["address"]
            result_data["latitude"] = item["latitude"]
            result_data["longitude"] = item["longitude"]
            for details in item["historical"]:
                datetime_object = datetime.strptime(details["time"], "%Y-%m-%dT%H:%M:%SZ")
                datetimeNewFormat = datetime_object.strftime("%Y%m%d%H%M")
                datetime_object_formatted = datetime.strptime(datetimeNewFormat,"%Y%m%d%H%M")
                temp_historical = {}
                if (datetime_object_formatted>=delay_time_formatted and datetime_object_formatted<=curr_time_formatted):
                    temp_historical = {
                                        "available_bike_stands" : details["available_bike_stands"], 
                                        "bike_stands" : details["bike_stands"],
                                        "time" : details["time"]
                                            }
                    result_data["historical"].append(temp_historical)
            list_result_data.append(result_data)
    # print(list_result_data)
    return list_result_data


# Main
# save_historic_data_in_DB(2)
# temp = final_result(datetime.strptime("20210210","%Y%m%d"))
# print(temp[1])

# bikedata_minutes()
# for  item in BikeStands.objects(name="CITY QUAY"):
#     for j in item.historical:
#         print(j["time"])

# fetch_Data_from_DB_for_minutes(10)
# fetch_Data_from_DB_for_day(1)
save_historic_data_in_DB(5)

save_Bike_Stands_Location()
# print(fetch_Bike_Stands_Location())