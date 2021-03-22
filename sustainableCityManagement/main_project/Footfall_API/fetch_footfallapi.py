import sys
# from ..Logs.service_logs import bus_log
from .store_bus_routes_data_in_database import StoreBusRoutesData
# from ..Config.config_handler import read_config
from datetime import datetime, timedelta
import copy
# from collections import Counter
# import collections
import json

class FetchBusApi:
    def __init__(self):
        self.busRoutesObj = StoreBusRoutesData()
    
    def bus_stand_locations(self):
        result_response = {}
        all_stops = self.busRoutesObj.fetch_busstops_location()
        counter = 0
        for location in all_stops:
            stop_custom_id = "stop_"+str(counter)
            result_response[stop_custom_id] = {}
            result_response[stop_custom_id]["STOP_NAME"] = location["stop_name"]
            result_response[stop_custom_id]["STOP_LAT"] = location["stop_lat"]
            result_response[stop_custom_id]["STOP_LON"] = location["stop_lon"]
            counter += 1
        return result_response