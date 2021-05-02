import sys
# from ..Logs.service_logs import bus_log
from .store_footfall_data_in_database import StoreFootfallData
from ..Config.config_handler import read_config
from datetime import datetime, timedelta
import copy
from ..ML_models import footfall_prediction as predictor
# from collections import Counter
# import collections

import json

config_vals = read_config("Footfall_API")


class FootfallApi:
    def __init__(self):
        self.FootfallObj = StoreFootfallData()

    # Structure the footfalls data in required format to send it to frontend
    def footfall_datebased_graphvalues_predictions(self, required_location, days_interval=config_vals["days_interval_size"]):
        result_response = {}
        footfall_count_arr = []
        footfall_dateBased, last_date = self.FootfallObj.fetch_data_from_db_with_prediction(
            days_interval, required_location)
        prediction_date = datetime.strftime(
            last_date + timedelta(days=1), "%Y-%m-%d")
        for item in footfall_dateBased:
            location = required_location
            result_response[location] = {}
            for data in item["footfall_data"]:
                date = datetime.strftime(data["data_date"], "%Y-%m-%d")
                result_response[location][date] = data["count"]
                footfall_count_arr.append(data["count"])
        predicted_val = predictor.predict_footfall(footfall_count_arr)
        result_response[required_location][prediction_date] = predicted_val
        return result_response

# Structure the overall footfalls data in required format to send it to frontend
    def footfall_overall(self):
        result_response = {}
        footfall_overall = self.FootfallObj.fetch_footfall_overall()
        counter = 0
        with open(config_vals["footfall_locations_file"], "r") as f:
            loaded_locations = json.load(f)
            for item in footfall_overall:
                location = item["location"]
                result_response[location] = {}
                result_response[location]["Footfall"] = item["count"]
                result_response[location]["Lat"] = loaded_locations[location]["lat"]
                result_response[location]["Lon"] = loaded_locations[location]["lon"]
        return result_response

