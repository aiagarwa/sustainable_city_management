from main_project.Emergency_Service_API import fetch_emergency_service
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import StoreServiceData
from django.test import TestCase
from unittest.mock import MagicMock
from mock import patch
import json
import datetime
from freezegun import freeze_time


@freeze_time("2021-03-11 17")
class TestFetchEmergencyServiceApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_fire_stations_data(self):
        fire_stations_data_class = fetch_emergency_service.FetchEmergencyServiceApi()
        store_fire_service_data_to_database = StoreServiceData()
        mocked_result = [
            {
                "station_name": "station_0",
                "station_address": "test_name_1",
                "station_phone": "+ 353 700899",
                "station_email": "y@dublin.com",
                "service_type": "emergency",
                "station_lat": "35.33",
                "station_lon": "34.33"
            },
            {
                "station_name": "station_1",
                "station_address": "test_name_2",
                "station_phone": "+ 353 700889",
                "station_email": "y@dublin.com",
                "service_type": "emergency",
                "station_lat": "39.33",
                "station_lon": "32.33"
            }
        ]
        store_fire_service_data_to_database.fetch_fire_station_informations = MagicMock(
            return_value=mocked_result)
        expected_result = {
            "Station_0": {
                "STATION_NAME": "station_0",
                "STATION_ADDRESS": "test_name_1",
                "STATION_PHONE": "+ 353 700899",
                "STATION_EMAIL": "y@dublin.com",
                "SERVICE_TYPE": "emergency",
                "STATION_LAT": "35.33",
                "STATION_LON": "34.33"
            },

            "Station_1": {
                "STATION_NAME": "station_1",
                "STATION_ADDRESS": "test_name_2",
                "STATION_PHONE": "+ 353 700889",
                "STATION_EMAIL": "y@dublin.com",
                "SERVICE_TYPE": "emergency",
                "STATION_LAT": "39.33",
                "STATION_LON": "32.33"
            }
        }
        result = fire_stations_data_class.fire_stations_data(
            fireStationObj=store_fire_service_data_to_database)
        self.assertDictEqual(result, expected_result)

    def test_health_centers_data(self):
        fetch_health_center_class = fetch_emergency_service.FetchEmergencyServiceApi()
        store_health_center_data_to_database = StoreServiceData()
        mocked_result = [
            {
                "center_name": "315_IJ",
                "center_address": "dublin",
                "center_phone": "+353 08999",
                "center_lat": 25.39,
                "center_lon": 25.38
            },
            {
                "center_name": "315_2J",
                "center_address": "dublin",
                "center_phone": "+353 08979",
                "center_lat": 20.39,
                "center_lon": 20.38
            }
        ]
        store_health_center_data_to_database.fetch_health_center_informations = MagicMock(
            return_value=mocked_result)

        expected_result = {
            "Health_Center_0": {
                "CENTER_NAME": "315_IJ",
                "CENTER_ADDRESS": "dublin",
                "CENTER_PHONE": "+353 08999",
                "CENTER_LAT": 25.39,
                "CENTER_LONG": 25.38
            },

            "Health_Center_1": {
                "CENTER_NAME": "315_2J",
                "CENTER_ADDRESS": "dublin",
                "CENTER_PHONE": "+353 08979",
                "CENTER_LAT": 20.39,
                "CENTER_LONG": 20.38
            }
        }
        result = fetch_health_center_class.health_centers_data(
            healthCentersObj=store_health_center_data_to_database)
        self.assertDictEqual(result, expected_result)

    def test_garda_stations_data(self):
        garda_stations_data_class = fetch_emergency_service.FetchEmergencyServiceApi()

        store_garda_service_data_to_database = StoreServiceData()

        mocked_result = [
            {
                "station": "station_0",
                "station_address": "test_name_1",
                "station_division": "main",
                "station_divisional_hq": "Dublin",
                "station_phone": "+ 353 700899",
                "station_lat": "35.73",
                "station_lon": "34.93"
            },
            {
                "station": "station_1",
                "station_address": "test_name_2",
                "station_division": "main",
                "station_divisional_hq": "Dublin",
                "station_phone": "+ 353 700898",
                "station_lat": "30.73",
                "station_lon": "30.93"
            }
        ]
        store_garda_service_data_to_database.fetch_garda_station_informations = MagicMock(
            return_value=mocked_result)

        expected_result = {
            "Garda_Station_0": {
                "STATION_NAME": "station_0",
                "STATION_ADDRESS": "test_name_1",
                "STATION_DIVISION": "main",
                "STATION_DIVISIONAL_HQ": "Dublin",
                "STATION_PHONE": "+ 353 700899",
                "STATION_LAT": "35.73",
                "STATION_LON": "34.93"
            },

            "Garda_Station_1": {
                "STATION_NAME": "station_1",
                "STATION_ADDRESS": "test_name_2",
                "STATION_DIVISION": "main",
                "STATION_DIVISIONAL_HQ": "Dublin",
                "STATION_PHONE": "+ 353 700898",
                "STATION_LAT": "30.73",
                "STATION_LON": "30.93"
            }
        }

        result = garda_stations_data_class.garda_stations_data(
            gardaStationsObj=store_garda_service_data_to_database)
        self.assertDictEqual(result, expected_result)

    def test_hospitals_data(self):
        fetch_hospital_class = fetch_emergency_service.FetchEmergencyServiceApi()
        store_hospital_data_to_database = StoreServiceData()
        mocked_result = [
            {
                "center_name": "315_IJ",
                "center_address": "dublin",
                "center_lat": 25.39,
                "center_lon": 25.38
            },
            {
                "center_name": "315_2J",
                "center_address": "dublin",
                "center_lat": 20.39,
                "center_lon": 20.38
            }
        ]
        store_hospital_data_to_database.fetch_hospital_informations = MagicMock(
            return_value=mocked_result)

        expected_result = {
            "Hospital_0": {
                "CENTER_NAME": "315_IJ",
                "CENTER_ADDRESS": "dublin",
                "CENTER_LAT": 25.39,
                "CENTER_LONG": 25.38
            },

            "Hospital_1": {
                "CENTER_NAME": "315_2J",
                "CENTER_ADDRESS": "dublin",
                "CENTER_LAT": 20.39,
                "CENTER_LONG": 20.38
            }
        }
        result = fetch_hospital_class.hospitals_data(
            hospitalsObj=store_hospital_data_to_database)
        self.assertDictEqual(result, expected_result)
