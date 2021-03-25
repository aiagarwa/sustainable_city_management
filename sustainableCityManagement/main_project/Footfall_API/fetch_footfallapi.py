import sys
# from ..Logs.service_logs import bus_log
from .store_footfall_data_in_database import StoreFootfallData
# from ..Config.config_handler import read_config
from datetime import datetime, timedelta
import copy
# from collections import Counter
# import collections
import json

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

    def footfall_overall(self):
        result_response = {}
        footfall_overall = self.FootfallObj.fetch_footfall_overall()
        counter = 0
        for item in footfall_overall:
            location = item["location"]
            result_response[location] = {}
            result_response[location]["Footfall"] = item["count"]
            result_response[location]["Lat"] = "to-be-added"
            result_response[location]["Lon"] = "to-be-added"
        return result_response

# obj = FootfallApi()
# print(obj.footfall_datebased("2021-01-03","2021-01-05"))
# print(obj.footfall_overall())