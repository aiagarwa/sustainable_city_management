import sys
from mongoengine import *
import requests
import json
from datetime import datetime, timedelta
import pytz
from ..Logs.service_logs import bike_log
from ..Config.config_handler import read_config
from ..Bike_API.bike_collections_db import BikeStands
from ..Bike_API.bike_collections_db import BikeAvailability
from ..Bike_API.bike_collections_db import BikesStandsLocation
import logging

# Calling logging function for bike _API
logger = bike_log()
config_vals = read_config("Bike_API")


class StoreBikeDataToDatabase:

    #  This method all locations of bike stands in db.
    def save_bike_stands_location(self):
        url = config_vals["stations_api_url"]
        payload = {}
        headers = {}
        # Fetching response from the URL.
        try:
            response = requests.get(url, headers=headers, data=payload)
            loc_result = json.loads(response.text)
            for item in loc_result:
                standLocations = BikesStandsLocation(
                    name=item["st_NAME"], latitude=item["st_LATITUDE"], longitude=item["st_LONGITUDE"])
                try:
                    standLocations.save()
                except:
                    pass
            logger.info('Bike stand locations stored into DB successfully.')
        except:
            logger.exception('Storing bike stand location into DB failed!')
            raise

    # This method fetch the data from bike api for each day

    def get_bikedata_day(self, days_historical):
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
            response = requests.get(url, headers=headers, data=payload)
            tmp_result = json.loads(response.text)
            return tmp_result
        except:
            logger.exception('Not able to fetch data from API')
            raise

    # This method fetch the live data from bike api (default timespan: 5 minutes)

    def get_bikedata_live(self, minutes_delay):
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
            response = requests.get(url, headers=headers, data=payload)
            tmp_result = json.loads(response.text)
            return tmp_result
        except:
            logger.exception('Not able to fetch data from API')
            raise

    # This method saves the locations for Bike Usage in DB

    def bike_usage_save_locations(self, days_historical):
        bikeusagedata = self.get_bikedata_day(days_historical)
        try:
            for item in bikeusagedata:
                bikestands = BikeStands(name=item["name"])
                try:
                    bikestands.save()
                except:
                    pass
            logger.info(
                'Bike stand locations for Bike Usage stored into DB successfully.')
        except:
            logger.exception(
                'Storing bike stand location for Bike Usage into DB failed!')
            raise


# This method gets the data from API for a single day and store in DB.

    def bikedata_day(self, days_historical):
        bikeusagedata = self.get_bikedata_day(days_historical)
        try:
            for item in bikeusagedata:
                bikestands = BikeStands.objects(name=item["name"]).first()
                if bikestands is not None:
                    for stand_details in item["historic"]:
                        datetimeConvert = datetime.strptime(
                            stand_details["time"], "%Y-%m-%dT%H:%M:%SZ")
                        bikesAvailability = BikeAvailability(
                            bike_stands=stand_details["bike_stands"], available_bike_stands=stand_details["available_bike_stands"], time=datetimeConvert)
                        bikestands.historical.append(bikesAvailability)
                    bikestands.save()  # Saves Bike Availability Data
            logger.info('Bikestand data for days stored into DB successfully.')
        except:
            logger.exception('Storing bikestand data for days into DB failed!')
            raise

    # This method gets the data from API every 5 minutes and store in DB.
    def bikedata_minutes(self, minutes_delay=5):
        bikeusagedata = self.get_bikedata_live(minutes_delay)
        try:
            for item in bikeusagedata:
                bikestands = BikeStands.objects(name=item["name"]).first()
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
            logger.info(
                'Bikestand data for minutes stored into DB successfully.')
        except:
            logger.exception(
                'Storing bikestand data for minutes into DB failed!')
            raise

    # This method stores the data for n number of days in MongoDB

    def save_historic_data_in_db(self, days_historical):
        for i in range(days_historical):
            logger.info('Done extracting days = %d' % i)
            self.bike_usage_save_locations(i)
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


# a = StoreBikeDataToDatabase
# a.get_bikedata_day(3, 1)
