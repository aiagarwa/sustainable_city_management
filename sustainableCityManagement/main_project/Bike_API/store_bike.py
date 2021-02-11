from mongoengine import *
import requests
import json
from datetime import datetime, timedelta

# Connect to Database
connect('sustainableCityManagement', host='mongodb://127.0.0.1:27017/sustainableCityManagement')

# Define Embedded Document structure to store in Mongo DB. This contains Data related to Bikes availability. This is used by Bikestands Document
class BikeAvailability(EmbeddedDocument):
    available_bike_stands = IntField()
    available_bikes = IntField()
    time = StringField(max_length=200)

# Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity 
class BikeStands(Document):
    address = StringField(max_length=200, required=True)
    historical = ListField(EmbeddedDocumentField(BikeAvailability))
    latitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    longitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    name = StringField(max_length=200)
    meta = {'collection': 'BikeUsage'}

# This method gets the data from API for a single day and store in DB.
def bikedata(days_historical):
    now_time = datetime.now()
    curr_time = (now_time - timedelta(days=days_historical)).strftime("%Y%m%d%H%M") 
    url = ""
    delay_time =  (now_time - timedelta(days=days_historical + 1)).strftime("%Y%m%d%H%M")
    url = "https://dublinbikes.staging.derilinx.com/api/v1/resources/historical/?dfrom="+str(delay_time)+"&dto="+str(curr_time)
    payload={} 
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload) # Fetching response from the URL.
    result_response = {} # Storing end result.
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
                bikesAvailability = BikeAvailability(available_bike_stands = stand_details["available_bike_stands"], available_bikes = stand_details["available_bikes"], time = stand_details["time"])
                bikestands.historical.append(bikesAvailability)
            bikestands.save() # Saves Bike Availability Data
        else:
            print("Empty")

# This method stores the data for n number of days in MongoDB
def save_historic_data_in_DB(days_historical):
    for i in range(1,days_historical+1):
        bikedata(i)

# This method returns the Bikes availablity data for all locations (Bike Stands) for a particular day
def final_result(dateForData):
    q_set = BikeStands.objects() # Fetch Data from DB
    json_data = q_set.to_json() # Converts the Bikes Data from DB into JSON format
    dicts = json.loads(json_data)
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
                temp_historical = {}
                if (datetime_object.year == dateForData.year and  datetime_object.month == dateForData.month and datetime_object.day == dateForData.day):
                    datetimeNewFormat = datetime_object.strftime("%d%m%Y%H%M")
                    temp_historical = {
                                        "available_bikes" : details["available_bikes"], 
                                        "available_bike_stands" : details["available_bike_stands"],
                                        "time" : datetimeNewFormat
                                            }
                    result_data["historical"].append(temp_historical)
            list_result_data.append(result_data)

    return list_result_data

# Main
save_historic_data_in_DB(2)
temp = final_result(datetime.strptime("20210210","%Y%m%d"))
print(temp[1])

    