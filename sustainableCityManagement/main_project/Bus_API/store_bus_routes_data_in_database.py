import sys
from mongoengine import *
import requests
import json
import pytz
import csv
host_db = "mongodb://127.0.0.1:27017/sustainableCityManagementTest"
connect("sustainableCityManagementTest", host=host_db)


class BusStops(Document):
    stop_name = StringField(max_length=200)
    stop_id = StringField(max_length=200, unique=True)
    stop_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    stop_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'Bus_Stops'}
#     # logger.info('BusUsage document created successfully.')

class StoreBusRoutesData:
    def read_bus_stops(self):
        readfile = []
        with open("../sustainableCityManagement/main_project/Bus_API/resources/stops.csv", "r", encoding='utf-8') as f:
        # with open("./resources/stops.csv", "r") as f:
            readfile = list(csv.reader(f))
        return readfile

    def store_bus_stops(self):
        readfile = self.read_bus_stops()

        for i in range(1,len(readfile)):
            busstops = BusStops(stop_id = readfile[i][0],
                                stop_name = readfile[i][1].split(",")[0],
                                stop_lat = readfile[i][2],
                                stop_lon = readfile[i][3])
            try:
                busstops.save()
            except:
                pass

    def fetch_busstops_location(self, locationName = "all"):
        q_set = BusStops.objects()  # Fetch Data from DB
        # Converts the Processed Bikes Data from DB into JSON format
        json_data = q_set.to_json()
        locations = json.loads(json_data)
        # if locations is None:
        #     logger.error('Location data not retrieved from DB')
        return locations


a = StoreBusRoutesData()
a.store_bus_stops()
# print(a.fetch_busstops_location()[0])