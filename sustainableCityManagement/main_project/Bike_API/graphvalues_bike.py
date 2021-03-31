import json
import collections
from collections import Counter
from datetime import datetime, timedelta
from ..Logs.service_logs import bike_log
from .store_bikedata_to_database import StoreBikeDataToDatabase
from .store_processed_bikedata_to_db import StoreProcessedBikeDataToDB
from ..Config.config_handler import read_config

# Calling logging function for bike _API
logger = bike_log()


config_vals = read_config("Bike_API")
if config_vals is None:
    logger.error('No data retrieved from config files.')

# Below function is used for calling the graph values for bike usage on the basis of location.

class GraphValuesBike:
    def graphvalue_call_locationbased(self, days_historical=config_vals["default_days_historic"],
                                        store_processed_bike_data_to_db = StoreProcessedBikeDataToDB()):
        if days_historical == 1 or days_historical == 0:
            error_str = 'Assign days_historic parameter >= 2.'
            logger.error(error_str)
            raise ValueError(error_str)

        now_time = datetime.now()
        day_ahead_tmp = (now_time - timedelta(days=-1)
                        ).strftime("%Y-%m-%dT00:00:00Z")
        day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
        resultDictionary = {}
        try:
            fetched_data = store_processed_bike_data_to_db.fetch_processed_data(days_historical)
            fetched_predicted = store_processed_bike_data_to_db.fetch_predicted_data(day_ahead_tmp)
            for loc in fetched_data:
                if loc["name"] != "ALL_LOCATIONS":
                    tmpDict = {}
                    for item2 in loc["data"]:
                        day = item2["day"].strftime("%Y-%m-%d")
                        tmpDict[day] = item2["in_use"]

                    for item in fetched_predicted:
                        if item["name"] == loc["name"]:
                            tmpDict[day_ahead] = item["data"]["in_use"]

                    tmpDict = dict(collections.OrderedDict(
                        sorted(tmpDict.items())))
                    resultDictionary[loc["name"]] = {
                        "TOTAL_STANDS": loc["data"][0]["total_stands"], "IN_USE": tmpDict}
            return resultDictionary
        except:
            logger.exception(
                'Failed to execute bikes usage based on location.Check overall location API.')
            raise

    # Below function is used for calling the graph values for overall bike usage over a given timespan and predict value a day ahead.


    def graphvalue_call_overall(self, days_historical=config_vals["default_days_historic"],
                                        store_processed_bike_data_to_db = StoreProcessedBikeDataToDB()):
        if days_historical == 1 or days_historical == 0:
            error_str = 'Assign days_historic parameter >= 2.'
            logger.error(error_str)
            raise ValueError(error_str)

        now_time = datetime.now()
        day_ahead_tmp = (now_time - timedelta(days=-1)
                        ).strftime("%Y-%m-%dT00:00:00Z")
        day_ahead = (now_time - timedelta(days=-1)).strftime("%Y-%m-%d")
        resultDictionary = {}
        try:
            fetched_data = store_processed_bike_data_to_db.fetch_processed_data(days_historical)
            fetched_predicted = store_processed_bike_data_to_db.fetch_predicted_data(day_ahead_tmp)
            tmpDict = {}
            for item in fetched_data[-1]["data"]:
                day = item["day"].strftime("%Y-%m-%d")
                tmpDict[day] = item["in_use"]
            tmpDict[day_ahead] = fetched_predicted[-1]["data"]["in_use"]
            tmpDict = dict(collections.OrderedDict(sorted(tmpDict.items())))
            resultDictionary["ALL_LOCATIONS"] = {"TOTAL_STANDS": fetched_data[-1]["data"][0]["total_stands"],
                                                "IN_USE": tmpDict}
            return resultDictionary
        except:
            logger.exception(
                'Failed to execute bikes usage based on location.Check overall location API.')
            raise
