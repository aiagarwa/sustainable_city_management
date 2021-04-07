from .store_bikedata_to_database import StoreBikeDataToDatabase
from ..ML_models.bikes_usage_prediction import predict_bikes_usage
from ..Config.config_handler import read_config
from ..Logs.service_logs import bike_log
from mongoengine import *
from datetime import datetime, timedelta
from ..Bike_API.bike_collections_db import BikeProcessedData
from ..Bike_API.bike_collections_db import BikeAvailabilityProcessedData
from ..Bike_API.bike_collections_db import BikePredictedData
from ..Bike_API.bike_collections_db import BikeAvailabilityPredictedData
from freezegun.api import FakeDatetime
import pytz

# Calling logging function for bike _API
logger = bike_log()
config_vals = read_config("Bike_API")

# This method gets the raw data from DB, process and store in different collection in DB.


class StoreProcessedBikeDataToDB:
    def fetch_bike_data(self, delay_time_formatted):
        store_bike_data_to_database = StoreBikeDataToDatabase()
        result = store_bike_data_to_database.fetch_data_from_db_for_day(
            delay_time_formatted)
        return result

    def store_bikedata(self, days_historical):
        now_time = datetime.now(pytz.utc)
        try:
            for i in range(days_historical):
                delay_time = (now_time - timedelta(days=i)
                              ).strftime("%Y%m%d%H%M")
                delay_time_formatted = datetime.strptime(
                    delay_time, "%Y%m%d%H%M")
                data_day = (now_time - timedelta(days=i)
                            ).strftime("%Y-%m-%dT00:00:00Z")
                data_day_formatted = datetime.strptime(
                    data_day, "%Y-%m-%dT%H:%M:%SZ")
                pipeline = [
                    {
                        "$unwind": "$data"
                    },
                    {"$match": {"data.day": data_day_formatted}}
                ]

                tmp_result = self.fetch_bike_data(delay_time_formatted)
                # Going through all the items in the fetched data from DB and storing the average of daily usage (Location based).
                for item in tmp_result:
                    # Get the number of documents with a particular location name
                    biketemp = BikeProcessedData._get_collection().count_documents({
                        'name': item["name"]})
                    if biketemp < 1:
                        bikedata = BikeProcessedData(name=item["name"])
                        bikedata.save()  # Saves Location details in MongoDB as a Document if it does not exist
                    else:
                        bikedata = BikeProcessedData(name=item["name"])
                    q_set = BikeProcessedData.objects(
                        name=item["name"]).aggregate(*pipeline)
                    if len(list(q_set)) < 1:
                        bikedata = bikedata._qs.filter(
                            name=item["name"]).first()
                        in_use_bikes_arr = []
                        for stand_details in item["historical"]:
                            in_use_bikes_arr.append(
                                stand_details["available_bike_stands"])
                            bikesAvailability = BikeAvailabilityProcessedData(day=(now_time - timedelta(days=i)).strftime(
                                "%Y-%m-%d"), total_stands=stand_details["bike_stands"], in_use=sum(in_use_bikes_arr)//len(in_use_bikes_arr))
                        bikedata.data.append(bikesAvailability)
                        bikedata.save()
            logger.info(
                "Processed bike data of daily usgae stored in DB successfully..")
        except:
            logger.exception(
                'Failed to process raw data for bikes usage based on location.Check data stored in raw DB.')
            raise

    # This method gets the raw data from DB, process and store as different collection in DB.

    def store_bikedata_all_locations(self, days_historical):
        now_time = datetime.now(pytz.utc)
        try:
            for i in range(days_historical):
                data_day = (now_time - timedelta(days=i)
                            ).strftime("%Y-%m-%dT00:00:00Z")
                data_day_formatted = datetime.strptime(
                    data_day, "%Y-%m-%dT%H:%M:%SZ")
                pipeline = [
                    {
                        "$unwind": "$data"
                    },
                    {"$match": {"data.day": data_day_formatted}}
                ]
                q_set = BikeProcessedData.objects().aggregate(*pipeline)
                list_q_set = list(q_set)
                total_stands_all_locations = 0
                in_use_all_locations = 0
                for item in list_q_set:
                    total_stands_all_locations = total_stands_all_locations + \
                        item["data"]["total_stands"]
                    in_use_all_locations = in_use_all_locations + \
                        item["data"]["in_use"]

            # Get the number of documents with a particular location name
                biketemp = BikeProcessedData._get_collection(
                ).count_documents({'name': "ALL_LOCATIONS"})
                if biketemp < 1:
                    bikedata = BikeProcessedData(name="ALL_LOCATIONS")
                    bikedata.save()  # Saves Location details in MongoDB as a Document if it does not exist
                else:
                    bikedata = BikeProcessedData(name="ALL_LOCATIONS")
                q_set = BikeProcessedData.objects(
                    name="ALL_LOCATIONS").aggregate(*pipeline)
                if len(list(q_set)) < 1:
                    bikedata = bikedata._qs.filter(
                        name="ALL_LOCATIONS").first()
                    bikesAvailability = BikeAvailabilityProcessedData(day=(now_time - timedelta(days=i)).strftime(
                        "%Y-%m-%d"), total_stands=total_stands_all_locations, in_use=in_use_all_locations)
                    bikedata.data.append(bikesAvailability)
                    bikedata.save()
            logger.info(
                'Processed data based on location stored in DB successfully.')
            return total_stands_all_locations
        except:
            logger.exception(
                'Failed to process raw data for bikes availability based on location.Check data stored in raw DB.')
            raise

    # To Create location list.

    def create_location_list(self):
        now_time = datetime.now(pytz.utc)
        data_day = (now_time - timedelta(days=1)
                    ).strftime("%Y-%m-%dT00:00:00Z")
        data_day_formatted = datetime.strptime(data_day, "%Y-%m-%dT%H:%M:%SZ")
        pipeline = [
            {
                "$unwind": "$data"
            },
            {"$match": {"data.day": data_day_formatted}}
        ]
        q_set = BikeProcessedData.objects().aggregate(*pipeline)
        list_q_set = list(q_set)
        train_data = []
        in_use_list = []
        for item in list_q_set:
            train_data_dict = {
                "name": item["name"], "in_use": in_use_list, "total": item["data"]["total_stands"]}
            train_data.append(train_data_dict)
        if train_data is None:
            logger.error(
                'Train data for location list is empty.Check for the availability of processed DB[Bikes] data ')
        return(train_data)

    def get_in_use_arr(self, days_historical):
        now_time = datetime.now(pytz.utc)
        train_data = self.create_location_list()
        for item in train_data:
            in_use_list = []
            for i in range(days_historical):
                data_day = (now_time - timedelta(days=i)
                            ).strftime("%Y-%m-%dT00:00:00Z")
                data_day_formatted = datetime.strptime(
                    data_day, "%Y-%m-%dT%H:%M:%SZ")
                pipeline = [
                    {
                        "$unwind": "$data"
                    },
                    {"$match": {"data.day": data_day_formatted}}
                ]
                q_set = BikeProcessedData.objects(
                    name=item["name"]).aggregate(*pipeline)
                list_location_details = list(q_set)
                for loc in list_location_details:
                    in_use_list.append(loc["data"]["in_use"])
            item["in_use"] = in_use_list
        if train_data is None:
            logger.error(
                'Train data for bike in use is empty.Check for the availability of processed DB[Bikes] data ')
        return train_data

    def store_predict_data_in_db(self, days_historical):
        now_time = datetime.now(pytz.utc)
        day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
        pipeline = [
            {
                "$unwind": "$data"
            },
            {"$match": {"data.day": day_ahead}}
        ]
        try:
            for item in self.get_in_use_arr(days_historical):
                # Get the number of documents with a particular location name
                biketemp = BikePredictedData._get_collection().count_documents({
                    'name': item["name"]})
                if biketemp < 1:
                    bikedata = BikePredictedData(name=item["name"])
                    bikedata.save()  # Saves Location details in MongoDB as a Document if it does not exist
                else:
                    bikedata = BikePredictedData(name=item["name"])
                q_set = BikePredictedData.objects(
                    name=item["name"]).aggregate(*pipeline)
                if len(list(q_set)) < 1:
                    bikesAvailability = BikeAvailabilityPredictedData(
                        day=day_ahead, total_stands=item["total"], in_use=predict_bikes_usage(item["in_use"]))
                    bikedata.data.append(bikesAvailability)
                    bikedata.save()
            logger.info(
                'Predicted data for day ahead stored in DB successfully.')
        except:
            logger.exception('Unable to store predicted data on to DB')
            raise

    def fetch_processed_data(self, days_historical):
        now_time = datetime.now(pytz.utc)
        curr_time = now_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        curr_time_formatted = datetime.strptime(
            curr_time, "%Y-%m-%dT%H:%M:%SZ")
        data_day = (now_time - timedelta(days=days_historical)
                    ).strftime("%Y-%m-%dT00:00:00Z")
        data_day_formatted = datetime.strptime(data_day, "%Y-%m-%dT%H:%M:%SZ")
        pipeline = [
            {"$project": {
                "data": {"$filter": {
                    "input": "$data",
                    "as": "data",
                    "cond": {"$and": [
                        {"$lte": ["$$data.day", curr_time_formatted]},
                        {"$gte": ["$$data.day", data_day_formatted]}
                    ]}
                }
                },
                "name":"$name",
                "_id":0}
             },
        ]
        q_set = BikeProcessedData.objects().aggregate(*pipeline)
        list_q_set = list(q_set)
        if list_q_set is None:
            logger.error(
                'No processed data for historical was retrieved. Check for the availability of processed DB[Bikes] data ')
        return list_q_set

    def fetch_predicted_data(self, predict_date):
        try:
            predict_date_formatted = datetime.strptime(
                predict_date, "%Y-%m-%dT%H:%M:%SZ")
        except:
            predict_date_formatted = FakeDatetime(2021, 4, 1, 0, 0)
        pipeline = [
            {
                "$unwind": "$data"
            },
            {"$match": {"data.day": predict_date_formatted}}
        ]
        q_set = BikePredictedData.objects().aggregate(*pipeline)
        list_q_set = list(q_set)
        if list_q_set is None:
            logger.error(
                'No processed data for predicted was retrieved. Check for the availability of processed DB[Bikes] data ')
        return list_q_set
