import sys
from datetime import datetime, timedelta
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


class BusTrips(Document):
    trip_id = StringField(max_length=200, unique=True)
    route_id = StringField(max_length=200)
    meta = {'collection': 'Bus_Trips'
            }


class BusTimings(Document):
    trip_id = StringField(max_length=200, unique=True)
    stop_id = StringField(max_length=200)
    stop_arrival_time = DateTimeField()
    stop_departure_time = DateTimeField()
    stop_sequence = IntField()
    meta = {'collection': 'Bus_Timings'
            }


class StoreBusRoutesData:

    def read_bus_stops(self):
        readfile = []
        with open("../sustainableCityManagement/main_project/Bus_API/resources/stops.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

    def store_bus_stops(self):
        readfile = self.read_bus_stops()
        for i in range(1, len(readfile)):
            busstops = BusStops(stop_id=readfile[i][0],
                                stop_name=readfile[i][1].split(",")[0],
                                stop_lat=readfile[i][2],
                                stop_lon=readfile[i][3])
            try:
                busstops.save()
            except:
                pass

    def fetch_busstops_location(self, locationName="all"):
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
        for i in range(1, len(readfile)):
            busroutes = BusRoutes(route_id=readfile[i][0],
                                  route_name=readfile[i][3])
            try:
                busroutes.save()
            except:
                pass

    def fetch_busroutes(self, locationName="all"):
        q_set = BusRoutes.objects()  # Fetch Data from DB
        # Converts the Processed Bus Data from DB into JSON format
        json_data = q_set.to_json()
        bus_routes = json.loads(json_data)
        if bus_routes is None:
            logger.error('Bus Routes data is not retrieved from DB')
        return bus_routes

    def read_bus_trips(self):
        readfile = []
        with open("../sustainableCityManagement/main_project/Bus_API/resources/trips.csv", "r", encoding="utf8") as f:
            # with open("./resources/routes.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

    def store_bus_trips(self):
        readfile = self.read_bus_trips()
        for i in range(1, len(readfile)):
            bustrips = BusTrips(route_id=readfile[i][0],
                                trip_id=readfile[i][2])
            try:
                bustrips.save()
            except:
                pass

    def fetch_bustrips(self, locationName="all"):
        q_set = BusTrips.objects()  # Fetch Data from DB
        # Converts the Processed Bus Data from DB into JSON format
        json_data = q_set.to_json()
        bus_trips = json.loads(json_data)
        if bus_trips is None:
            logger.error('Bus Trips data is not retrieved from DB')
        return bus_trips

    def read_bus_timings(self):
        readfile = []
        with open("../sustainableCityManagement/main_project/Bus_API/resources/stop_times.csv", "r", encoding="utf8") as f:
            # with open("./resources/routes.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

    def store_bus_timings(self):
        readfile = self.read_bus_timings()
        for i in range(1, len(readfile)):
            bustimings = BusTimings(trip_id=readfile[i][0], stop_id=readfile[i][3],
                                    stop_arrival_time=readfile[i][1], stop_departure_time=readfile[i][2], stop_sequence=readfile[i][4])
            try:
                bustimings.save()
            except:
                pass

    def fetch_bus_timings(self, locationName="all"):
        q_set = BusTimings.objects()  # Fetch Data from DB
        # Converts the Processed Bus Data from DB into JSON format
        json_data = q_set.to_json()
        bus_timings = json.loads(json_data)
        if bus_timings is None:
            logger.error('Bus Trips data is not retrieved from DB')
        return bus_timings

#a = StoreBusRoutesData()
# a.store_bus_timings()
# print(a.fetch_busstops_location()[:2])

# a.store_bus_routes()
# print(a.fetch_busroutes()[1])
