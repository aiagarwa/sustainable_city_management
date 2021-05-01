# -*- coding: utf-8 -*-
import sys
from mongoengine import *
import csv
import json
import math
from ..Logs.service_logs import parkings_log
from ..Parkings_Recreational_Places_API.recreational_places_parkings_collections_db import Parks, Cinemas, PlayingPitches, Beaches

class StoreRecreationalPlacesParkingsData:
    def __init__(self):
        self.logger = parkings_log()

# Method reads the csv file containing the information of beaches and return the list of details of beaches
    def read_beaches_locations(self):
        readfile = []
        self.logger.info("Reading Beaches file")
        with open("../sustainableCityManagement/main_project/Parkings_Recreational_Places_API/resources/Beaches.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the relevant beaches information in Database
    def store_beaches_locations(self):
        readfile = self.read_beaches_locations()
        self.logger.info("Storing Beaches Data in DB")
        for i in range(1, len(readfile)):
            parkings=self.get_parkings(float(readfile[i][2]),float(readfile[i][3]))
            beaches = Beaches(beach_id=readfile[i][0],
                                beach_name=readfile[i][1],
                                beach_lat=readfile[i][2],
                                beach_lon=readfile[i][3],
                                beach_parkings=parkings)
            try:
                beaches.save()
            except:
                pass

# Method fetches the beaches information from Database and returns it
    def fetch_beaches_location(self, locationName="all"):
        q_set = Beaches.objects()  # Fetch Data from DB
        # Converts the Beach Data from DB into JSON format
        json_data = q_set.to_json()
        beaches = json.loads(json_data)
        if beaches is None:
            self.logger.error('Beach data not retrieved from DB')
        else:
            self.logger.info("Retrieved Beaches from DB")
            for b in beaches:
                del b["_id"]
        return beaches

# Method reads the csv file containing the information of playing pitches and return the list of details of fplaying pitches
    def read_playing_pitches_locations(self):
        readfile = []
        self.logger.info("Reading Playing Pitches file")
        with open("../sustainableCityManagement/main_project/Parkings_Recreational_Places_API/resources/PlayingPitches.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the relevant playing pitches information in Database
    def store_playing_pitches_locations(self):
        readfile = self.read_playing_pitches_locations()
        self.logger.info("Storing Playing Pitches Data in DB")
        for i in range(1, len(readfile)):
            parkings=self.get_parkings(float(readfile[i][3]),float(readfile[i][4]))
            playing_pitches = PlayingPitches(facility_type=readfile[i][0],
                                facility_name=readfile[i][1],
                                facility_location=readfile[i][2],
                                facility_lat=readfile[i][3],
                                facility_lon=readfile[i][4],
                                facility_parkings=parkings)
            try:
                playing_pitches.save()
            except:
                pass


# Method fetches the playing pitches information from Database and returns it
    def fetch_playing_pitches_location(self, locationName="all"):
        q_set = PlayingPitches.objects()  # Fetch Data from DB
        json_data = q_set.to_json()
        playing_pitches = json.loads(json_data)
        if playing_pitches is None:
            self.logger.error('Playing Pitch data not retrieved from DB')
        else:
            self.logger.info("Retrieved Playing Pitches from DB")
            for p in playing_pitches:
                del p["_id"]
        return playing_pitches

 # Method reads the csv file containing the information of parks and return the list of details of parks
    def read_parks_locations(self):
        readfile = []
        self.logger.info("Reading Parks file")
        with open("../sustainableCityManagement/main_project/Parkings_Recreational_Places_API/resources/Parks.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the relevant parks information in Database
    def store_parks_locations(self):
        readfile = self.read_parks_locations()
        self.logger.info("Storing Parks Data in DB")
        for i in range(1, len(readfile)):
            parkings=self.get_parkings(float(readfile[i][3]),float(readfile[i][4]))
            parks = Parks(park_name=readfile[i][0],
                                park_address=readfile[i][1],
                                park_area=readfile[i][2],
                                park_lat=readfile[i][3],
                                park_lon=readfile[i][4],
                                park_parkings=parkings)
            try:
                parks.save()
            except:
                pass


# Method fetches the parks information from Database and returns it
    def fetch_parks_location(self, locationName="all"):
        q_set = Parks.objects()  # Fetch Data from DB
        # Converts the Parks Data from DB into JSON format
        json_data = q_set.to_json()
        parks = json.loads(json_data)
        if parks is None:
            self.logger.error('Parks data not retrieved from DB')
        else:
            self.logger.info("Retrieved Parks from DB")
            for p in parks:
                del p["_id"]
        return parks

# Method reads the csv file containing the information of cinemas and return the list of details of cinemas
    def read_cinemas_locations(self):
        readfile = []
        self.logger.info("Reading Cinemas file")
        with open("../sustainableCityManagement/main_project/Parkings_Recreational_Places_API/resources/Cinemas.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        return readfile

# Method stores the relevant cinemas information in Database
    def store_cinemas_locations(self):
        readfile = self.read_cinemas_locations()
        self.logger.info("Storing Cinemas Data in DB")
        for i in range(1, len(readfile)):
            parkings=self.get_parkings(float(readfile[i][2]),float(readfile[i][3]))
            cinemas = Cinemas(cinema_name=readfile[i][0],
                                cinema_address=readfile[i][1],
                                cinema_lat=readfile[i][2],
                                cinema_lon=readfile[i][3],
                                cinema_parkings=parkings)
            try:
                cinemas.save()
            except:
                pass


# Method fetches the cinemas information from Database and returns it
    def fetch_cinemas_location(self, locationName="all"):
        q_set = Cinemas.objects()  # Fetch Data from DB
        # Converts the Cinemas Data from DB into JSON format
        json_data = q_set.to_json()
        cinemas = json.loads(json_data)
        if cinemas is None:
            self.logger.error('Cinemas data not retrieved from DB')
        else:
            self.logger.info("Retrieved Cinemas from DB")
            for c in cinemas:
                del c["_id"]
        return cinemas

# Method to get the five nearest parkings to a particular location.
    def get_parkings(self,lat,lon):
        with open("../sustainableCityManagement/main_project/Parkings_Recreational_Places_API/resources/disabledparkings.csv", "r", encoding="utf8") as f:
            readfile = list(csv.reader(f))
        loc_parkings=[]
        for i in range(1, len(readfile)):
            lat_parkings = float(readfile[i][2])
            lon_parkings = float(readfile[i][3])
            R = 6371e3; # metres
            phi1 = lat_parkings * math.pi/180
            phi2 = lat * math.pi/180
            delta_phi = (lat-lat_parkings) * math.pi/180
            delta_lambda = (lon-lon_parkings) * math.pi/180
            a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            d = R * c
            if d < 2000.0:
                loc_parkings.append({
                            "road": readfile[i][1],
                            "lat": readfile[i][2],
                            "lng": readfile[i][3],
                            "distance": d
                            })
        if len(loc_parkings)>5:
            loc_parkings=sorted(loc_parkings, key=lambda d: d['distance'], reverse=False)
            return loc_parkings[:5]
        else:
            return loc_parkings
