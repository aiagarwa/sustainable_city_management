import sys
from .store_parkingsdata_to_database import StoreParkingsData
from datetime import datetime, timedelta
import copy
import json


# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).

class FetchParkingsApi:
    def __init__(self):
        self.parkingsApiObj = StoreParkingsData()

     # Structure the parkings availability data in required format to send it to frontend   
    def parkings_availability(self, startdate, enddate):
        # Parse datetime
        if startdate:
            startdate = datetime.strptime(startdate, "%Y-%m-%d")
        if enddate:
            enddate = datetime.strptime(enddate, "%Y-%m-%d")

        if not startdate and not enddate:
            # Live data if no startdate nor enddate
            res = json.loads(self.parkingsApiObj.store_parking_spaces_availability_live().to_json())
        elif startdate and not enddate:
            # Get data for one day
            res = json.loads(self.parkingsApiObj.fetch_data_from_db_for_day(startdate).to_json())
        else:
            # Get data for all days (average each day data)
            # Loop from startdate to enddate in parkingsApiObj dedicatedmethod
            res = self.parkingsApiObj.fetch_data_from_db_historical(startdate, enddate)
        
        if res:
            return res
        else:
            return []

# This method returns the Parking name, area and latitude and longitude
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