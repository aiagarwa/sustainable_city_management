import sys
from mongoengine import *
import requests
import json
import pytz
import csv

class BusStops(Document):
    stop_name = StringField(max_length=200)
    stop_id = StringField(max_length=200, unique=True)
    stop_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    stop_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'Bus_Stops'
    }

class BusRoutes(Document):
    route_name = StringField(max_length=200)
    route_id = StringField(max_length=200, unique=True)
    meta = {'collection': 'Bus_Routes'
    }

class StoreBusRoutesData:
    def __init__(self):
        host_db = "mongodb://127.0.0.1:27017/sustainableCityManagementTest"
        connect(db = "sustainableCityManagementTest", host=host_db

    def read_bus_stops(self):
        readfile = []
        with open("../sustainableCityManagement/main_project/Bus_API/resources/stops.csv", "r", encoding="utf8") as f:
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
        # Converts the Processed Bus Data from DB into JSON format
        json_data = q_set.to_json()
        bus_stops = json.loads(json_data)
        if bus_stops is None:
            logger.error('Bus Stops data not retrieved from DB')
        return bus_stops

    def read_bus_routes(self):
        readfile = []
        with open("../sustainableCityManagement/main_project/Bus_API/resources/routes.csv", "r", encoding="utf8") as f:
        # with open("./resources/routes.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

    def store_bus_routes(self):
        readfile = self.read_bus_routes()
        for i in range(1,len(readfile)):
            busroutes = BusRoutes(route_id = readfile[i][0],
                                route_name = readfile[i][3])
            try:
                busroutes.save()
            except:
                pass

    def fetch_busroutes(self, locationName = "all"):
        q_set = BusRoutes.objects()  # Fetch Data from DB
        # Converts the Processed Bus Data from DB into JSON format
        json_data = q_set.to_json()
        bus_routes = json.loads(json_data)
        if bus_routes is None:
            logger.error('Bus Routes data is not retrieved from DB')
        return bus_routes

# a = StoreBusRoutesData()
# a.store_bus_stops()
# print(a.fetch_busstops_location()[1])

# a.store_bus_routes()
# print(a.fetch_busroutes()[1])
