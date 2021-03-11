import sys
from mongoengine import *
import requests
import json
from datetime import datetime, timedelta
import pytz
from ..Logs.service_logs import bike_log
from ..Config.config_handler import read_config
import logging
# Calling logging function for bike _API
logger = bike_log()

# Connect to Database
try:
    config_vals = read_config("Bike_API")
    host_db = "mongodb://127.0.0.1:%d/%s" % (
        config_vals["db_port"], config_vals["db_name"])
    connect(config_vals["db_name"], host=host_db)
except:
    logger.exception('Unable to access Database')
    raise

# Define Embedded Document structure to store in Mongo DB. This contains Data related to Bikes availability. This is used by Bikestands Document


class BikeAvailability(EmbeddedDocument):
    bike_stands = IntField()
    available_bike_stands = IntField()
    time = DateTimeField()
    logger.info('BikeAvailability structure defined successfully.')
    # time = StringField(max_length=200) #, unique=True)

# Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity


class BikeStands(Document):
    historical = ListField(EmbeddedDocumentField(BikeAvailability))
    name = StringField(max_length=200)
    meta = {'collection': 'BikeUsage'}
    logger.info('BikeUsage document created successfully.')

# Define Document for location


class BikesStandsLocation(Document):
    name = StringField(max_length=200, required=True)
    latitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    longitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'BikeStandsLocation'}
    logger.info('BikesStandLocation document created successfully.')

class StoreBikeDataToDatabase:
    def save_bike_stands_location(self):
        url = config_vals["stations_api_url"]
        payload = {}
        headers = {}
        # Fetching response from the URL.
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            loc_result = json.loads(response.text)
            for item in loc_result:
                loctemp = BikesStandsLocation._get_collection().count_documents(
                    {'name': item["st_NAME"]})  # Get the number of documents with a particular location name
                if loctemp < 1:
                    standLocations = BikesStandsLocation(
                        name=item["st_NAME"], latitude=item["st_LATITUDE"], longitude=item["st_LONGITUDE"])
                    standLocations.save()
            logger.info('Bike stand location stored into DB successfully.')
        except:
            logger.exception('Storing bike stand location into DB failed!')
            raise
    # This method gets the data from API for a single day and store in DB.


    def bikedata_day(self, days_historical):
        now_time = datetime.now(pytz.utc)
        curr_time = (now_time - timedelta(days=days_historical)
                    ).strftime("%Y%m%d%H%M")
        delay_time = (now_time - timedelta(days=days_historical + 1)
                    ).strftime("%Y%m%d%H%M")
        url = config_vals["location_api_url"] + "?dfrom=" + \
            str(delay_time)+"&dto="+str(curr_time)
        payload = {}
        headers = {}
        # Fetching response from the URL.
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            tmp_result = json.loads(response.text)
            for item in tmp_result:
                # Get the number of documents with a particular location name
                biketemp = BikeStands._get_collection(
                ).count_documents({'name': item["name"]})
                if biketemp < 1:
                    bikestands = BikeStands(name=item["name"])
                    bikestands.save()  # Saves Location details in MongoDB as a Document if it does not exist
                else:
                    bikestands = BikeStands(name=item["name"])
                bikestands = bikestands._qs.filter(name=item["name"]).first()
                if bikestands is not None:
                    for stand_details in item["historic"]:
                        datetimeConvert = datetime.strptime(
                            stand_details["time"], "%Y-%m-%dT%H:%M:%SZ")
                        bikesAvailability = BikeAvailability(
                            bike_stands=stand_details["bike_stands"], available_bike_stands=stand_details["available_bike_stands"], time=datetimeConvert)
                        bikestands.historical.append(bikesAvailability)
                    bikestands.save()  # Saves Bike Availability Data
        except:
            logger.exception('Storing bikestand data for days into DB failed!')
            raise

    # This method gets the data from API every 5 minutes and store in DB.


    @staticmethod
    def bikedata_minutes(minutes_delay=5):
        now_time = datetime.now(pytz.utc)
        curr_time = now_time.strftime("%Y%m%d%H%M")
        url = ""
        delay_time = (now_time - timedelta(minutes=minutes_delay)
                    ).strftime("%Y%m%d%H%M")
        url = config_vals["location_api_url"] + "?dfrom=" + \
            str(delay_time)+"&dto="+str(curr_time)
        payload = {}
        headers = {}
        # Fetching response from the URL.
        try:
            response = requests.request("GET", url, headers=headers, data=payload)
            tmp_result = json.loads(response.text)
            for item in tmp_result:
                # Get the number of documents with a particular location name
                biketemp = BikeStands._get_collection(
                ).count_documents({'name': item["name"]})
                if biketemp < 1:
                    bikestands = BikeStands(name=item["name"])
                    bikestands.save()  # Saves Location details in MongoDB as a Document if it does not exist
                else:
                    bikestands = BikeStands(name=item["name"])
                bikestands = bikestands._qs.filter(name=item["name"]).first()
                if bikestands is not None:
                    for stand_details in item["historic"]:
                        datetimeConvert = datetime.strptime(
                            stand_details["time"], "%Y-%m-%dT%H:%M:%SZ")
                        pipeline = [
                            {
                                "$unwind": "$historical"
                            },
                            {"$match": {"historical.time": datetimeConvert}}
                        ]
                        q_set = BikeStands.objects(
                            name=item["name"]).aggregate(*pipeline)
                        data_exists = len(list(q_set))
                        if data_exists < 1:
                            bikesAvailability = BikeAvailability(
                                bike_stands=stand_details["bike_stands"], available_bike_stands=stand_details["available_bike_stands"], time=datetimeConvert)
                            bikestands.historical.append(bikesAvailability)
                    bikestands.save()  # Saves Bike Availability Data
            logger.info('Bikestand data for minutes stored into DB successfully.')
        except:
            logger.exception('Storing bikestand data for minutes into DB failed!')
            raise

    # This method stores the data for n number of days in MongoDB


    def save_historic_data_in_db(self, days_historical):
        for i in range(days_historical):
            logger.info('Done extracting days = %d' % i)
            self.bikedata_day(i)
        logger.info('Bike stand data for days stored in to DB successfully.')
    # Fetch Data for Locations


    def fetch_bike_stands_location(self):
        q_set = BikesStandsLocation.objects()  # Fetch Data from DB
        # Converts the Processed Bikes Data from DB into JSON format
        json_data = q_set.to_json()
        locations = json.loads(json_data)
        if locations is None:
            logger.error('Location data not retrieved from DB')
        return locations

    # Fetch bikedata from db for a particular date


    def fetch_data_from_db_for_day(self, dateForData):
        start_date_str = dateForData.strftime("%Y-%m-%dT00:00:00Z")
        end_date_str = dateForData.strftime("%Y-%m-%dT23:59:59Z")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%SZ")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%SZ")
        pipeline = [
            {"$project": {
                "historical": {"$filter": {
                    "input": "$historical",
                    "as": "historical",
                    "cond": {"$and": [
                        {"$lte": ["$$historical.time", end_date]},
                        {"$gte": ["$$historical.time", start_date]}
                    ]}
                }
                },
                "name": "$name",
                "_id": 0}
            },
        ]
        q_set = BikeStands.objects().aggregate(*pipeline)  # Fetch Data from DB
        list_q_set = list(q_set)
        if list_q_set is None:
            logger.error('Bikedata for day not retrieved from DB')
        return list_q_set

    # This method returns the Bikes availablity data for all locations (Bike Stands) for last few minutes


    def fetch_data_from_db_for_minutes(self):
        # now_time = datetime.now(pytz.utc)
        # curr_time = now_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        # curr_time_formatted = datetime.strptime(curr_time, "%Y-%m-%dT%H:%M:%SZ")
        # delay_time = (now_time - timedelta(minutes=minutes)
        #               ).strftime("%Y-%m-%dT%H:%M:%SZ")
        # delay_time_formatted = datetime.strptime(delay_time, "%Y-%m-%dT%H:%M:%SZ")
        # pipeline = [
        #     {"$project": {
        #         "historical": {"$filter": {
        #             "input": "$historical",
        #             "as": "historical",
        #             "cond": {"$and": [
        #                 {"$lte": ["$$historical.time", curr_time_formatted]},
        #                 {"$gte": ["$$historical.time", delay_time_formatted]}
        #             ]}
        #         }
        #         },
        #         "name":"$name",
        #         "_id":0}
        #      },
        # ]
        pipeline = [
            {"$unwind": "$historical"},
            {"$sort": {"historical.time": 1}},
            {"$group": {"_id": "$_id", "name": {"$first": "$name"},
                        "historical": {"$push": "$historical"}}},
            {"$project": {
                "historical": {"$slice": ["$historical", -1]
                            },
                "name":"$name",
                "_id":0}
            },
        ]
        q_set = BikeStands.objects().aggregate(
            *pipeline, allowDiskUse=True)  # Fetch Data from DB
        q_set = list(q_set)
        if len(q_set) == 0:
            logger.error('Bikedata for minutes not retrieved from DB')
        # print(list(q_set))
        return (q_set)
