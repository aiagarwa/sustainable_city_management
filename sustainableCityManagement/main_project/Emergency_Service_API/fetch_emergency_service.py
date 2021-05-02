import sys
from .store_emergency_service_data_in_database import *
from main_project.Logs.service_logs import emergency_service_log
from datetime import datetime, timedelta
import copy
import json


class FetchEmergencyServiceApi:
    def __init__(self):
        self.logger = emergency_service_log()
        self.pd = pd

    # Structure the fire stations data in required format to send it to frontend
    def fire_stations_data(self, fireStationObj=StoreServiceData()):
        result_response = {}
        all_stations = fireStationObj.fetch_fire_station_informations(self)
        counter = 0
        for items in all_stations:
            station_custom_id = "Station_"+str(counter)
            result_response[station_custom_id] = {}
            result_response[station_custom_id]["STATION_NAME"] = items["station_name"]
            result_response[station_custom_id]["STATION_ADDRESS"] = items["station_address"]
            result_response[station_custom_id]["STATION_PHONE"] = items["station_phone"]
            result_response[station_custom_id]["STATION_EMAIL"] = items["station_email"]
            result_response[station_custom_id]["SERVICE_TYPE"] = items["service_type"]
            result_response[station_custom_id]["STATION_LAT"] = items["station_lat"]
            result_response[station_custom_id]["STATION_LON"] = items["station_lon"]
            counter += 1
        return result_response

 # Structure the health centers data in required format to send it to frontend
    def health_centers_data(self, healthCentersObj=StoreServiceData()):
        result_response = {}
        counter = 0
        all_centers = healthCentersObj.fetch_health_center_informations(self)
        for items in all_centers:
            centers_custom_id = "Health_Center_"+str(counter)
            result_response[centers_custom_id] = {}
            result_response[centers_custom_id]["CENTER_NAME"] = items["center_name"]
            result_response[centers_custom_id]["CENTER_ADDRESS"] = items["center_address"]
            result_response[centers_custom_id]["CENTER_PHONE"] = items["center_phone"]
            result_response[centers_custom_id]["CENTER_LAT"] = items["center_lat"]
            result_response[centers_custom_id]["CENTER_LONG"] = items["center_lon"]
            counter += 1
        return result_response

 # Structure the garda stations data in required format to send it to frontend
    def garda_stations_data(self, gardaStationsObj=StoreServiceData()):
        result_response = {}
        counter = 0
        all_station = gardaStationsObj.fetch_garda_station_informations()
        for items in all_station:
            station_custom_id = "Garda_Station_"+str(counter)
            result_response[station_custom_id] = {}
            result_response[station_custom_id]["STATION_NAME"] = items["station"]
            result_response[station_custom_id]["STATION_ADDRESS"] = items["station_address"]
            result_response[station_custom_id]["STATION_DIVISION"] = items["station_division"]
            result_response[station_custom_id]["STATION_DIVISIONAL_HQ"] = items["station_divisional_hq"]
            result_response[station_custom_id]["STATION_PHONE"] = items["station_phone"]
            result_response[station_custom_id]["STATION_LAT"] = items["station_lat"]
            result_response[station_custom_id]["STATION_LON"] = items["station_lon"]
            counter += 1
        return result_response

 # Structure the hospitals data in required format to send it to frontend
    def hospitals_data(self, hospitalsObj=StoreServiceData()):
        result_response = {}
        counter = 0
        all_centers = hospitalsObj.fetch_hospital_informations()
        for items in all_centers:
            centers_custom_id = "Hospital_"+str(counter)
            result_response[centers_custom_id] = {}
            result_response[centers_custom_id]["CENTER_NAME"] = items["center_name"]
            result_response[centers_custom_id]["CENTER_ADDRESS"] = items["center_address"]
            result_response[centers_custom_id]["CENTER_LAT"] = items["center_lat"]
            result_response[centers_custom_id]["CENTER_LONG"] = items["center_lon"]
            counter += 1
        return result_response
