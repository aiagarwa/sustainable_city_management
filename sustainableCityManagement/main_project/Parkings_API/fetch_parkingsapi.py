import sys
# from ..Logs.service_logs import bus_log
from .store_parkingsdata_to_database import StoreParkingsData
# from ..Config.config_handler import read_config
from datetime import datetime, timedelta
import copy
# from collections import Counter
# import collections
import json

# Calling logging function for bike _API
# logger = bike_log()

# Calling Config values for processing api.
# config_vals = read_config("Bus_API")
# if config_vals is None:
#     logger.error('No data retrieved from config files.')

# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).

class FetchParkingsApi:
    def __init__(self):
        self.parkingsApiObj = StoreParkingsData()
    
    def parkings_availability(self, startdate, enddate):
        # Parse datetime
        if startdate:
            startdate = datetime.strptime(startdate, "%Y-%m-%d")
        if enddate:
            enddate = datetime.strptime(enddate, "%Y-%m-%d")

        if not startdate and not enddate:
            # Live data if no startdate nor enddate
            res = self.parkingsApiObj.get_parkings_spaces_availability_live()
        elif startdate and not enddate:
            # Get data for one day
            print("day")
            res = self.parkingsApiObj.fetch_data_from_db_for_day(startdate)
        else:
            # Get data for all days (average each day data)
            # Loop from startdate to enddate in parkingsApiObj dedicatedmethod
            res = self.parkingsApiObj.fetch_data_from_db_historical(startdate, enddate)
        
        if res:
            return json.loads(res.to_json())
        else:
            return []

    def parkings_locations(self):
        return [
            {
                "name": "PARNELL",
                "area": "Northwest",
                "lat": 53.350810,
                "lng": -6.268310
            },
            {
                "name": "ILAC",
                "area": "Northwest",
                "lat": 53.348610,
                "lng": -6.268840
            },
            {
                "name": "JERVIS",
                "area": "Northwest",
                "lat": 53.348780,
                "lng": -6.266670
            },
            {
                "name": "ARNOTTS",
                "area": "Northwest",
                "lat": 53.349080,
                "lng": -6.260060
            },
            {
                "name": "MARLBORO",
                "area": "Northeast",
                "lat": 53.352600098081375,
                "lng": -6.258366086014968
            },
            {
                "name": "ABBEY",
                "area": "Northeast",
                "lat": 53.35024325062157,
                "lng": -6.254233328658077
            },
            {
                "name": "THOMASST",
                "area": "Southwest",
                "lat": 53.34381779026483,
                "lng": -6.2802188590302395
            },
            {
                "name": "C/CHURCH",
                "area": "Southwest",
                "lat": 53.3433754859322,
                "lng": -6.269683162040512
            },
            {
                "name": "SETANTA",
                "area": "Southeast",
                "lat": 53.342046862254755,
                "lng": -6.256021086015311
            },
            {
                "name": "DAWSON",
                "area": "Southeast",
                "lat": 53.340471400850085,
                "lng": -6.256018776761035
            },
            {
                "name": "TRINITY",
                "area": "Southeast",
                "lat": 53.34416060960417,
                "lng": -6.262745776634299
            },
            {
                "name": "GREENRCS",
                "area": "Southeast",
                "lat": 53.342438538176374,
                "lng": -6.263818974717609
            },
            {
                "name": "DRURY",
                "area": "Southeast",
                "lat": 53.342987236356,
                "lng": -6.2631027690892935
            },
            {
                "name": "B/THOMAS",
                "area": "Southeast",
                "lat": 53.34268459927202,
                "lng": -6.261434643686948
            }
        ]