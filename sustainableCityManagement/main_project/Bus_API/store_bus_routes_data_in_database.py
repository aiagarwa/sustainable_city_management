import sys
from datetime import datetime, timedelta
from mongoengine import *
import requests
import json
import pytz
import csv
import time as time
import pandas as pd
from ..Logs.service_logs import bus_log
from ..Bus_API.bus_collections_db import BusStops, BusTimings, BusRoutes, BusTrips, StopsInfo, BusPath, Coordinate


class StoreBusRoutesData:
    def __init__(self):
        self.logger = bus_log()
        self.pd = pd

# Method reads the csv file containing the information of bus stops and return the list of details of busstops
    def read_bus_stops(self):
        readfile = []
        self.logger.info("Reading Bus Stops file")
        with open("../sustainableCityManagement/main_project/Bus_API/resources/stops.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the relevant bus stops information in Database
    def store_bus_stops(self):
        readfile = self.read_bus_stops()
        self.logger.info("Storing Bus Stops Data in DB")
        for i in range(1, len(readfile)):
            busstops = BusStops(stop_id=readfile[i][0],
                                stop_name=readfile[i][1].split(",")[0],
                                stop_lat=readfile[i][2],
                                stop_lon=readfile[i][3])
            try:
                busstops.save() # Store Data in DB
            except:
                pass

# Method fetches the bus stops information from Database and returns list of bus stops details
    def fetch_busstops_location(self):
        q_set = BusStops.objects()  # Fetch Data from DB
        json_data = q_set.to_json()
        bus_stops = json.loads(json_data)
        if bus_stops is None:
            self.logger.error('Bus Stops data not retrieved from DB')
        else:
            self.logger.info("Retrieved Bus Stops from DB")
        return bus_stops

# Method reads the bus routes information from csv and returns it as list
    def read_bus_routes(self):
        readfile = []
        self.logger.info("Reading Bus Routes file")
        with open("../sustainableCityManagement/main_project/Bus_API/resources/routes.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the bus routes information in Database
    def store_bus_routes(self):
        readfile = self.read_bus_routes()
        self.logger.info("Storing Bus Routes Data in DB")
        for i in range(1, len(readfile)):
            busroutes = BusRoutes(route_id=readfile[i][0],
                                  route_name=readfile[i][3])
            try:
                busroutes.save() # Store Data in DB
            except:
                pass

# Method fetches the bus routes information from Database and returns it
    def fetch_busroutes(self):
        q_set = BusRoutes.objects()  # Fetch Data from DB
        json_data = q_set.to_json()
        bus_routes = json.loads(json_data)
        if bus_routes is None:
            self.logger.error('Bus Routes data is not retrieved from DB')
        else:
            self.logger.info("Retrieved Bus Routes from DB")
        return bus_routes

# Method reads the bus trips information from csv and returns it as list
    def read_bus_trips(self):
        readfile = []
        self.logger.info("Reading Bus Trips file")
        with open("../sustainableCityManagement/main_project/Bus_API/resources/trips.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the bus trips information in Database
    def store_bus_trips(self):
        readfile = self.read_bus_trips()
        self.logger.info("Storing Bus Trips Data in DB")
        for i in range(1, len(readfile)):
            bustrips = BusTrips(route_id=readfile[i][0],
                                trip_id=readfile[i][2])
            try:
                bustrips.save() #Storing data in DB
            except:
                pass
    
# Method stores the bus timings at each stop in Database
    def store_bus_times(self):
        fields = ['trip_id', 'arrival_time','departure_time','stop_id','stop_sequence']
        readfile = self.pd.read_csv("../sustainableCityManagement/main_project/Bus_API/resources/stop_times.csv",encoding="utf8",
                        dtype={'trip_id':"string",'arrival_time':"string",'departure_time':"string",'stop_id':"string",'stop_sequence':'int8'},
                        usecols=fields
                        )
        self.logger.info("Storing Arrival and Departure Timings for Bus Trips in DB")
        for i in readfile.index:
            trips = BusTrips.objects(trip_id=readfile["trip_id"][i]).first()
            if trips is not None:
                stopsInfo = StopsInfo(stop_id=readfile["stop_id"][i], stop_arrival_time=readfile["arrival_time"][i],
                                        stop_departure_time=readfile["departure_time"][i], stop_sequence=readfile["stop_sequence"][i])
                trips.stops.append(stopsInfo) 
                trips.save() # Storing data in DB

# Method fetches and returns the bus trips information from Database
    def fetch_bustrips(self):
        q_set = BusTrips.objects()  # Fetch Data from DB
        json_data = q_set.to_json() 
        bus_trips = json.loads(json_data)
        if bus_trips is None:
            self.logger.error('Bus Trips data is not retrieved from DB')
        else:
            self.logger.info("Retrieved Bus Trips from DB")
        return bus_trips

# Method reads the bus paths information from json file
    def read_bus_paths(self):
        data = []
        self.logger.info("Reading Bus Paths file")
        with open("../sustainableCityManagement/main_project/Bus_API/resources/trips_paths.json", "r", encoding="utf8") as f:
            data = json.loads(f.read())
        return data

# Methods storing bus paths details in DB
    def store_bus_paths(self):
        data = self.read_bus_paths()
        self.logger.info("Storing Bus Paths Data in DB")
        
        for path in data['paths']:
            start = path['start']
            end = path['end']
            bus_path = BusPath(_id = start+end, start_stop_id = start, end_stop_id = end)

            coordinates = path['coordinates']
            for coordinate in coordinates:
                coordinate_obj = Coordinate(lat = coordinate[0], lon = coordinate[1])
                bus_path.coordinates.append(coordinate_obj)
            bus_path.save()

  # Methods fetches bus path details from db and return as list  
    def fetch_bus_paths(self):
        q_set = BusPath.objects()  # Fetch Data from DB
        # Converts the Processed Bus Data from DB into JSON format
        json_data = q_set.to_json()
        bus_paths = json.loads(json_data)
        if bus_paths is None:
            self.logger.error('Bus Paths data not retrieved from DB')
        else:
            self.logger.info("Retrieved Bus Paths from DB")
        return bus_paths
