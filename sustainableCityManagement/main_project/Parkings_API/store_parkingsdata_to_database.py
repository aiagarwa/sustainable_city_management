import sys
from mongoengine import *
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pytz
from ..Logs.service_logs import bike_log
from ..Config.config_handler import read_config
import logging
# Calling logging function for Parkings_API
logger = bike_log()
# config_vals = read_config("Parkings_API")


# Define Document Structure to store in Mongo DB. This contains Data related to Parking Spaces
class ParkingAvailability(EmbeddedDocument):
    name = StringField(max_length=200)
    area = StringField(max_length=200) # Deprecated
    availableSpaces = IntField()

class ParkingsAvailability(Document):
    updateTimestamp = DateTimeField(unique=True)
    parkings = ListField(EmbeddedDocumentField(ParkingAvailability))
    meta = {'collection': 'ParkingsAvailability'}

class StoreParkingsData:

    # This method fetch the live data from parkings spaces API (default timespan: ~5 minutes)
    def get_parkings_spaces_availability_live(self):
        try:
            response = requests.request("GET", "https://opendata.dublincity.ie/TrafficOpenData/CP_TR/CPDATA.xml")
            parkingSpaces = ET.fromstring(response.text)

            timestamp = parkingSpaces[-1].text
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

            return parkingsAvailability
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
        
        list_q_set = list(q_set)
        # Average-out
        # ...
        if list_q_set is None:
            logger.error('Parkings data for day not retrieved from DB')
        return list_q_set
    
    
    def fetch_data_from_db_historical(self, dateFrom, dateTo):
        # For each day between dateFrom and dateTo, fetch "fetch_data_from_db_for_day"
        return None

parking = StoreParkingsData()
# parking.get_parkings_spaces_availability_live()

print(parking.fetch_data_from_db_for_day(datetime(2021, 3, 23)))