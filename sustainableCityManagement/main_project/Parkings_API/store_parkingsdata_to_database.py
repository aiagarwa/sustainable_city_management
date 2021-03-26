import sys
from mongoengine import *
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
from ..Logs.service_logs import bike_log
from ..Config.config_handler import read_config
from ..Parkings_API.parkings_collections_db import ParkingsAvailability,ParkingAvailability
import json
import logging
import statistics
# Calling logging function for Parkings_API
logger = bike_log()
# config_vals = read_config("Parkings_API")

class StoreParkingsData:

    # This method fetch the live data from parkings spaces API (default timespan: ~5 minutes)
    def get_parkings_spaces_availability_live(self):
        try:
            response = requests.request("GET", "https://opendata.dublincity.ie/TrafficOpenData/CP_TR/CPDATA.xml")
            parkingSpaces = ET.fromstring(response.text)
            timestamp = parkingSpaces[-1].text

            # If data already present for that timestamp, return from db
            q_set = ParkingsAvailability.objects(updateTimestamp=timestamp)
            if q_set:
                return q_set

            # Else parse, store and return new data
            else:
                parkings = []
                for area in parkingSpaces:
                    areaName = area.tag.upper()
                    if areaName != "TIMESTAMP":
                        for parking in area:
                            name = parking.attrib["name"].upper()
                            try:
                                spaces = int(parking.attrib["spaces"])
                            except:
                                spaces = None

                            parkings.append(ParkingAvailability(area=areaName, name=name, availableSpaces=spaces))
                
                parkingsAvailability = ParkingsAvailability(updateTimestamp=timestamp, parkings=parkings)
                parkingsAvailability.save()

                return [parkingsAvailability]
        except:
            logger.exception('Not able to fetch data from API')
            raise


    # Fetch parkings availaility from db for a particular date
    def fetch_data_from_db_for_day(self, dateForData):
        start_date_str = dateForData.strftime("%Y-%m-%dT00:00:00Z")
        end_date_str = dateForData.strftime("%Y-%m-%dT23:59:59Z")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%SZ")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%dT%H:%M:%SZ")
        
        q_set = ParkingsAvailability.objects(updateTimestamp__gte=start_date, updateTimestamp__lte=end_date)
        return q_set
    
    
    def fetch_data_from_db_historical(self, dateFrom, dateTo):
        # For each day between dateFrom and dateTo, fetch "fetch_data_from_db_for_day"
        res = []
        for dayDate in self.daterange(dateFrom, dateTo):
            q_set = self.fetch_data_from_db_for_day(dayDate)
            
            if not q_set:
                continue
            
            dayAvgSpaces = {}
            for parkingsAvailability in q_set:
                for parkingAvailability in parkingsAvailability["parkings"]:

                    if not parkingAvailability["name"] in dayAvgSpaces:
                        dayAvgSpaces[parkingAvailability["name"]] = []
                        
                    # If available space is not None (i.e. missing data)
                    if parkingAvailability["availableSpaces"]:
                        dayAvgSpaces[parkingAvailability["name"]].append(parkingAvailability["availableSpaces"])

            # Average day's availability values for each parking
            for parkingName in dayAvgSpaces:
                if dayAvgSpaces[parkingName]:
                    dayAvgSpaces[parkingName] = int(statistics.mean(dayAvgSpaces[parkingName]))
                else:
                    dayAvgSpaces[parkingName] = None # If no available data to compute average

            res.append({
                "_id": { "$oid": None },
                "updateTimestamp": {
                    "$date": dayDate
                },
                "parkings": dayAvgSpaces
            })

        return res
    

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)