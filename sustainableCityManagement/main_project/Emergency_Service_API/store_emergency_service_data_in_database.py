import sys
from datetime import datetime, timedelta
from mongoengine import *
import requests
import json
import pytz
import csv
import time as time
import pandas as pd
from main_project.Logs.service_logs import emergency_service_log

# Structure of collection storing Firestations details
class FireStations(Document):
    station_name = StringField(max_length=200, unique=True)
    station_address = StringField(max_length=200)
    station_phone = StringField(max_length=200)
    station_email = StringField(max_length=200)
    service_type = StringField(max_length=200)
    station_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    station_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'Fire_Service'
            }

# Structure of collection storing Health Centers details
class HealthCenters(Document):
    center_name = StringField(max_length=200, unique=True)
    center_address = StringField(max_length=200)
    center_email = StringField(max_length=200)
    center_phone = StringField(max_length=200)
    center_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    center_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'Health_Centers'
            }

# Structure of collection storing Garda Stations details
class GardaStations(Document):
    station = StringField(max_length=200)
    station_address = StringField(max_length=200)
    station_phone = StringField(max_length=200)
    station_division = StringField(max_length=200)
    station_divisional_hq = StringField(max_length=200)
    station_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    station_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'Garda_Station'
            }

# Structure of collection storing Hospitals details
class Hospitals(Document):
    center_name = StringField(max_length=200, unique=True)
    center_address = StringField(max_length=200)
    center_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    center_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'Hospitals'
            }


class StoreServiceData:
    def __init__(self):
        self.logger = emergency_service_log()
        self.pd = pd

# Method reads the csv file containing the information of fire stations and return the list of details of fire stations
    def read_fire_stations(self):
        readfile = []
        self.logger.info("Reading fire stations file")
        with open("../sustainableCityManagement/main_project/Emergency_Service_API/resources/fcc_fire_stations_dublin.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the relevant fire stations information in Database
    def store_fire_stations(self):
        readfile = self.read_fire_stations()
        self.logger.info("Storing fire stations Data in DB")
        for i in range(1, len(readfile)):
            firestations = FireStations(station_name=readfile[i][0],
                                        station_address=readfile[i][1],
                                        station_phone=readfile[i][2],
                                        station_email=readfile[i][3],
                                        service_type=readfile[i][5],
                                        station_lat=readfile[i][6],
                                        station_lon=readfile[i][7])
            try:
                firestations.save()
            except:
                pass

# Method fetches the fire stations information from Database and returns list of fire stations details
    def fetch_fire_station_informations(self, locationName="all"):
        q_set = FireStations.objects()  # Fetch Data from DB
        # Converts the Fire stations Data from DB into JSON format
        json_data = q_set.to_json()
        fire_stations = json.loads(json_data)
        if fire_stations is None:
            self.logger.error('Fire stations data not retrieved from DB')
        else:
            self.logger.info("Retrieved fire stations from DB")
        return fire_stations


# Method reads the csv file containing the information of health centers and return the list of details of health centers
    def read_health_centers(self):
        readfile = []
        self.logger.info("Reading health centers file")
        with open("../sustainableCityManagement/main_project/Emergency_Service_API/resources/fcc_health_centers_dublin.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the relevant health centers information in Database
    def store_health_centers(self):
        readfile = self.read_health_centers()
        self.logger.info("Storing health centers Data in DB")
        for i in range(1, len(readfile)):
            healthcenters = HealthCenters(center_name=readfile[i][0],
                                          center_address=readfile[i][1] + readfile[i][2] +
                                          readfile[i][3] + readfile[i][4],
                                          center_phone=readfile[i][5],
                                          center_lat=readfile[i][8],
                                          center_lon=readfile[i][9])
            try:
                healthcenters.save()
            except:
                pass

# Method fetches the health centers information from Database and returns list of health centers details
    def fetch_health_center_informations(self, locationName="all"):
        q_set = HealthCenters.objects()  # Fetch Data from DB
        # Converts the Health Centers Data from DB into JSON format
        json_data = q_set.to_json()
        health_centers = json.loads(json_data)
        if health_centers is None:
            self.logger.error('Health centers data is not retrieved from DB')
        else:
            self.logger.info("Retrieved health centers from DB")
        return health_centers


# Method reads the csv file containing the information of garda stations and return the list of details of garda stations
    def read_garda_stations(self):
        readfile = []
        self.logger.info("Reading Garda Stations file")
        with open("../sustainableCityManagement/main_project/Emergency_Service_API/resources/garda_stations_dublin.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the relevant garda stations information in Database
    def store_garda_stations(self):
        readfile = self.read_garda_stations()
        self.logger.info("Storing Garda stations Data in DB")
        for i in range(1, len(readfile)):
            garda_stations = GardaStations(station=readfile[i][0], station_address=readfile[i][1] + readfile[i][2] + readfile[i][3], station_phone=readfile[i]
                                           [4], station_division=readfile[i][6], station_divisional_hq=readfile[i][7], station_lat=readfile[i][13], station_lon=readfile[i][14])
            garda_stations.save()
        return garda_stations

# Method fetches the garda stations information from Database and returns list of garda stations details
    def fetch_garda_station_informations(self):
        q_set = GardaStations.objects()  # Fetch Data from DB
        # Converts the Processed Bus Data from DB into JSON format
        json_data = q_set.to_json()
        garda_stations = json.loads(json_data)
        if garda_stations is None:
            self.logger.error('Bus Trips data is not retrieved from DB')
        else:
            self.logger.info("Retrieved Bus Trips from DB")
        return garda_stations

# Method reads the csv file containing the information of hospitals and return the list of details of hospitals
    def read_hospitals(self):
        readfile = []
        self.logger.info("Reading Hospitals file")
        with open("../sustainableCityManagement/main_project/Emergency_Service_API/resources/list_of_hospitals_in_ireland.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the relevant hospitals information in Database
    def store_hospitals(self):
        readfile = self.read_hospitals()
        self.logger.info("Storing Hospitals Data in DB")
        for i in range(1, len(readfile)):
            if "Dublin" in readfile[i][1]:
                hospitals_data = Hospitals(center_name=readfile[i][0],
                                           center_address=readfile[i][1],
                                           center_lat=readfile[i][3],
                                           center_lon=readfile[i][4])
                try:
                    hospitals_data.save()
                except:
                    pass

# Method fetches the hospitals information from Database and returns list of garda stations details
    def fetch_hospital_informations(self):
        q_set = Hospitals.objects()  # Fetch Data from DB
        # Converts the Processed Hospitals Data from DB into JSON format
        json_data = q_set.to_json()
        hospitals_data = json.loads(json_data)
        if hospitals_data is None:
            self.logger.error('Hospitals data is not retrieved from DB')
        else:
            self.logger.info("Retrieved Hospitals Data from DB")
        return hospitals_data
