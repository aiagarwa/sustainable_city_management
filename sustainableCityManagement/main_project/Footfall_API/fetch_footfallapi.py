import sys
# from ..Logs.service_logs import bus_log
from .store_footfall_data_in_database import StoreFootfallData
from ..Config.config_handler import read_config
from datetime import datetime, timedelta
import copy
# from collections import Counter
# import collections

import json

config_vals = read_config("Footfall_API")

class FootfallApi:
    def __init__(self):
        self.FootfallObj = StoreFootfallData()
    
    def footfall_datebased(self, start_date, end_date):
        result_response = {}
        footfall_dateBased = self.FootfallObj.fetch_data_from_db_for_day(start_date,end_date)
        for item in footfall_dateBased:
            location = item["location"]
            result_response[location] = {}
            for data in item["footfall_data"]:
                date = datetime.strftime(data["data_date"],"%Y-%m-%d")
                result_response[location][date] = data["count"]
        return result_response


    def footfall_datebased_graphvalues_predictions(self, days_interval = config_vals["days_interval_size"]):
        result_response = {}
        end_date = self.FootfallObj.get_last_date()
        start_date = datetime.strftime(datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=days_interval),"%Y-%m-%d")
        footfall_dateBased = self.FootfallObj.fetch_data_from_db_for_day(start_date,end_date)
        for item in footfall_dateBased:
            location = item["location"]
            result_response[location] = {}
            for data in item["footfall_data"]:
                date = datetime.strftime(data["data_date"],"%Y-%m-%d")
                result_response[location][date] = data["count"]
        return result_response




    def footfall_overall(self):
        result_response = {}
        footfall_overall = self.FootfallObj.fetch_footfall_overall()
        counter = 0
        with open(config_vals["footfall_locations_file"],"r") as f:
            loaded_locations = json.load(f)
            for item in footfall_overall:
                location = item["location"]
                result_response[location] = {}
                result_response[location]["Footfall"] = item["count"]
                result_response[location]["Lat"] = loaded_locations[location]["lat"]
                result_response[location]["Lon"] = loaded_locations[location]["lon"]
        return result_response

obj = FootfallApi()
obj.footfall_datebased_graphvalues_predictions()
# print(obj.footfall_overall())