from .store_bikedata_to_database import fetch_data_from_db_for_day
from .store_bikedata_to_database import fetch_data_from_db_for_minutes
from .store_bikedata_to_database import fetch_bike_stands_location
from ..ML_models.bikes_usage_prediction import predict_bikes_usage
from mongoengine import *
from datetime import datetime, timedelta
import pytz

# Connect to Database
connect('sustainableCityManagement', host='mongodb://127.0.0.1:27017/sustainableCityManagement')

# Define Embedded Document structure to store in Mongo DB. This contains Data related to Bikes availability. This is used by Bikestands Document
class BikeAvailabilityProcessedData(EmbeddedDocument):
    total_stands = IntField()
    in_use = IntField()
    day = DateField() 

# Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity 
class BikeProcessedData(Document):
    data = ListField(EmbeddedDocumentField(BikeAvailabilityProcessedData))
    name = StringField(max_length=200) 
    meta = {'collection': 'BikeUsageProcessed'}

# Define Embedded Document structure to store in Mongo DB. This contains Data related to Bikes availability. This is used by Bikestands Document
class BikeAvailabilityPredictedData(EmbeddedDocument):
    total_stands = IntField()
    in_use = IntField()
    day = DateField() 

# Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity 
class BikePredictedData(Document):
    data = ListField(EmbeddedDocumentField(BikeAvailabilityPredictedData))
    name = StringField(max_length=200) 
    meta = {'collection': 'BikeUsagePredict'}

# This method gets the raw data from DB, process and store in different collection in DB.
def store_bikedata(days_historical):
    now_time = datetime.now(pytz.utc)
    for i in range(days_historical):
        delay_time =  (now_time - timedelta(days=i)).strftime("%Y%m%d%H%M")
        delay_time_formatted = datetime.strptime(delay_time,"%Y%m%d%H%M")
        data_day = (now_time - timedelta(days=i)).strftime("%Y-%m-%dT00:00:00Z")
        data_day_formatted = datetime.strptime(data_day, "%Y-%m-%dT%H:%M:%SZ")
        pipeline = [
        {
            "$unwind":"$data"
        } ,  
        { "$match" : { "data.day" : data_day_formatted} } 
        ]
        tmp_result = fetch_data_from_db_for_day(delay_time_formatted)
        # Going through all the items in the fetched data from DB and storing the average of daily usage (Location based).
        for item in tmp_result:
            biketemp = BikeProcessedData._get_collection().count_documents({ 'name': item["name"] }) # Get the number of documents with a particular location name
            if biketemp < 1 :
                bikedata = BikeProcessedData(name = item["name"])
                bikedata.save()  # Saves Location details in MongoDB as a Document if it does not exist
            else:
                bikedata = BikeProcessedData(name = item["name"])
            q_set = BikeProcessedData.objects(name=item["name"]).aggregate(*pipeline)
            if len(list(q_set)) < 1 :
                bikedata = bikedata._qs.filter(name = item["name"]).first()
                in_use_bikes_arr = []
                for stand_details in item["historical"]:
                    in_use_bikes_arr.append(stand_details["available_bike_stands"])
                    bikesAvailability = BikeAvailabilityProcessedData(day = (now_time - timedelta(days=i)).strftime("%Y-%m-%d"), total_stands = stand_details["bike_stands"], in_use = sum(in_use_bikes_arr)//len(in_use_bikes_arr))
                bikedata.data.append(bikesAvailability)
                bikedata.save()

# This method gets the raw data from DB, process and store in different collection in DB.
def store_bikedata_all_locations(days_historical):
    now_time = datetime.now(pytz.utc)
    for i in range(days_historical):
        data_day = (now_time - timedelta(days=i)).strftime("%Y-%m-%dT00:00:00Z")
        data_day_formatted = datetime.strptime(data_day, "%Y-%m-%dT%H:%M:%SZ")
        pipeline = [
        {
            "$unwind":"$data"
        } ,  
        { "$match" : { "data.day" : data_day_formatted} } 
        ]
        q_set = BikeProcessedData.objects().aggregate(*pipeline)
        list_q_set = list(q_set)
        total_stands_all_locations = 0
        in_use_all_locations = 0
        for item in list_q_set:
            total_stands_all_locations = total_stands_all_locations + item["data"]["total_stands"]
            in_use_all_locations = in_use_all_locations + item["data"]["in_use"]
        biketemp = BikeProcessedData._get_collection().count_documents({ 'name': "ALL_LOCATIONS" }) # Get the number of documents with a particular location name
        if biketemp < 1 :
            bikedata = BikeProcessedData(name = "ALL_LOCATIONS")
            bikedata.save()  # Saves Location details in MongoDB as a Document if it does not exist
        else:
            bikedata = BikeProcessedData(name = "ALL_LOCATIONS")
        q_set = BikeProcessedData.objects(name="ALL_LOCATIONS").aggregate(*pipeline)
        if len(list(q_set)) < 1 :
            bikedata = bikedata._qs.filter(name = "ALL_LOCATIONS").first()
            bikesAvailability = BikeAvailabilityProcessedData(day = (now_time - timedelta(days=i)).strftime("%Y-%m-%d"), total_stands = total_stands_all_locations, in_use = in_use_all_locations)
            bikedata.data.append(bikesAvailability)
            bikedata.save()

def create_location_list():
    now_time = datetime.now(pytz.utc)
    data_day = (now_time - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    data_day_formatted = datetime.strptime(data_day, "%Y-%m-%dT%H:%M:%SZ")
    pipeline = [
    {
        "$unwind":"$data"
    } ,  
    { "$match" : { "data.day" : data_day_formatted} } 
    ]
    q_set = BikeProcessedData.objects().aggregate(*pipeline)
    list_q_set = list(q_set)
    train_data = []
    in_use_list = []
    for item in list_q_set:
        train_data_dict = {"name":item["name"],"in_use":in_use_list,"total":item["data"]["total_stands"]}
        train_data.append(train_data_dict)
    return(train_data)

def get_in_use_arr(days_historical):
    now_time = datetime.now(pytz.utc)
    train_data = create_location_list()
    for item in train_data:
        in_use_list = []
        for i in range(days_historical):
            data_day = (now_time - timedelta(days=i)).strftime("%Y-%m-%dT00:00:00Z")
            data_day_formatted = datetime.strptime(data_day, "%Y-%m-%dT%H:%M:%SZ")
            pipeline = [
            {
                "$unwind":"$data"
            } ,  
            { "$match" : { "data.day" : data_day_formatted} } 
            ]
            q_set = BikeProcessedData.objects(name=item["name"]).aggregate(*pipeline)
            list_location_details = list(q_set)
            for loc in list_location_details:
                in_use_list.append(loc["data"]["in_use"])
        item["in_use"] = in_use_list
    return train_data

def store_predict_data_in_db(days_historical):
    now_time = datetime.now(pytz.utc)
    day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
    pipeline = [
        {
            "$unwind":"$data"
        } ,  
        { "$match" : { "data.day" : day_ahead} } 
        ]
    for item in get_in_use_arr(days_historical):
        biketemp = BikePredictedData._get_collection().count_documents({ 'name': item["name"] }) # Get the number of documents with a particular location name
        if biketemp < 1 :
            bikedata = BikePredictedData(name = item["name"])
            bikedata.save()  # Saves Location details in MongoDB as a Document if it does not exist
        else:
            bikedata = BikePredictedData(name = item["name"])
        q_set = BikePredictedData.objects(name=item["name"]).aggregate(*pipeline)
        if len(list(q_set)) < 1 :
            bikesAvailability = BikeAvailabilityPredictedData(day = day_ahead, total_stands = item["total"], in_use = predict_bikes_usage(item["in_use"], previous_days_to_consider = days_historical - 1))
            bikedata.data.append(bikesAvailability)
            bikedata.save()

def fetch_processed_data(days_historical):
    now_time = datetime.now(pytz.utc)
    for i in range(days_historical):
        data_day = (now_time - timedelta(days=i)).strftime("%Y-%m-%dT00:00:00Z")
        data_day_formatted = datetime.strptime(data_day, "%Y-%m-%dT%H:%M:%SZ")
        pipeline = [
        {
            "$unwind":"$data"
        } ,  
        { "$match" : { "data.day" : data_day_formatted} } 
        ]
        q_set = BikeProcessedData.objects().aggregate(*pipeline)
        list_q_set = list(q_set)
    print(list_q_set)
    return list_q_set

def fetch_predicted_data(predict_date):
    predict_date_formatted = datetime.strptime(predict_date, "%Y-%m-%dT%H:%M:%SZ")
    pipeline = [
    {
        "$unwind":"$data"
    } ,  
    { "$match" : { "data.day" : predict_date_formatted} } 
    ]
    q_set = BikePredictedData.objects().aggregate(*pipeline)
    list_q_set = list(q_set)
    print(list_q_set)
    return list_q_set

# store_bikedata(5)
# store_bikedata_all_locations(5)
# store_predict_data_in_db(5)




# # fetch_processed_data(5)
now_time = datetime.now(pytz.utc)
predict_date = (now_time - timedelta(days=-1)).strftime("%Y-%m-%dT00:00:00Z")
fetch_predicted_data(predict_date)