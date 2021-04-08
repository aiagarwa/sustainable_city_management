import pandas as pd
from datetime import datetime, timedelta, date
from django.test import TestCase
from unittest.mock import MagicMock
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import StoreServiceData
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import FireStations
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import HealthCenters
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import GardaStations
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import Hospitals
from mongoengine import *
import mongomock as mm
from decimal import Decimal
import json


class TestStoreServiceData(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    # Testing firestation functions over database.

    def test_read_fire_stations(self):
        read_services = StoreServiceData()
        assert read_services.read_fire_stations()[0] == [
            'Name', 'Address', 'Phone', 'Email', 'Website', 'Fire_Service', 'LAT', 'LONG']
        assert read_services.read_fire_stations(
        )[1][0] == "Balbriggan Fire Station"

    def test_store_fire_stations(self):
        store_service = StoreServiceData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ["Balbriggan Fire Station",
                               "Balbriggan Enterprise and Trade Centre Harry Reynolds Road Balbriggan Co. Dublin", "+353 1 6734000", "fire@dublincity.ie", "x.com", "Dublin Fire Brigade - Foxtrot District", 0.78656, -0.1563]]

        store_service.read_fire_stations = MagicMock(
            return_value=expectedresult)
        store_service.store_fire_stations()

        fetch_fire_service = FireStations.objects(
            station_name="Balbriggan Fire Station").first()

        assert fetch_fire_service["station_address"] == "Balbriggan Enterprise and Trade Centre Harry Reynolds Road Balbriggan Co. Dublin"
        assert fetch_fire_service["station_phone"] == "+353 1 6734000"
        assert fetch_fire_service["station_email"] == "fire@dublincity.ie"
        assert fetch_fire_service["service_type"] == "Dublin Fire Brigade - Foxtrot District"
        self.assertAlmostEqual(
            fetch_fire_service["station_lat"], Decimal(0.786), None, None, 0.001)
        self.assertAlmostEqual(
            fetch_fire_service["station_lon"], Decimal(-0.156), None, None, 0.001)

    def test_fetch_fire_station_informations(self):
        fetch_service_fire = StoreServiceData()
        expectedresult = [[], ["Balbriggan Fire Station",
                               "Balbriggan Enterprise and Trade Centre Harry Reynolds Road Balbriggan Co. Dublin", "+353 1 6734000", "fire@dublincity.ie", "x.com", "Dublin Fire Brigade - Foxtrot District", 0.78656, -0.1563]]

        fetch_service_fire.read_fire_stations = MagicMock(
            return_value=expectedresult)
        fetch_service_fire.store_fire_stations()

        fire_service_loc = fetch_service_fire.fetch_fire_station_informations()

        assert fire_service_loc[0]["station_name"] == "Balbriggan Fire Station"
        assert fire_service_loc[0]["station_address"] == "Balbriggan Enterprise and Trade Centre Harry Reynolds Road Balbriggan Co. Dublin"
        assert fire_service_loc[0]["station_phone"] == "+353 1 6734000"
        assert fire_service_loc[0]["station_email"] == "fire@dublincity.ie"
        assert fire_service_loc[0]["service_type"] == "Dublin Fire Brigade - Foxtrot District"
        self.assertAlmostEqual(
            fire_service_loc[0]["station_lat"], 0.786, None, None, 0.002)
        self.assertAlmostEqual(
            fire_service_loc[0]["station_lon"], -0.156, None, None, 0.002)

    # Testing healthcenters functions over database.
    def test_read_health_centers(self):
        read_services = StoreServiceData()
        assert read_services.read_health_centers()[0] == [
            'Name', 'Address1', 'Address2', 'Address3', 'Address4', 'Phone', 'Email', 'Website', 'LAT', 'LONG']
        assert read_services.read_health_centers(
        )[1][0] == "Balbriggan Health Centre"

    def test_store_health_center_informations(self):
        store_service = StoreServiceData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ['Balbriggan Health Centre', 'Hampton Street,', 'Balbriggan,',
                               'Co. Dublin', 'end', '+353 1 8834906', 'sample@dublin.com', 'y.com', 0.78656, -0.1563]]

        store_service.read_health_centers = MagicMock(
            return_value=expectedresult)
        store_service.store_health_centers()

        fetch_health_service = HealthCenters.objects(
            center_name="Balbriggan Health Centre").first()
        assert fetch_health_service["center_address"] == "Hampton Street,Balbriggan,Co. Dublinend"
        assert fetch_health_service["center_phone"] == "+353 1 8834906"
        self.assertAlmostEqual(
            fetch_health_service["center_lat"], Decimal(0.786), None, None, 0.001)
        self.assertAlmostEqual(
            fetch_health_service["center_lon"], Decimal(-0.156), None, None, 0.001)

    def test_fetch_health_center_informations(self):
        fetch_service = StoreServiceData()

        expectedresult = [[],  ['Balbriggan Health Centre', 'Hampton Street,', 'Balbriggan,',
                                'Co. Dublin', 'end', '+353 1 8834906', 'sample@dublin.com', 'y.com', 0.78656, -0.1563]]
        fetch_service.read_health_centers = MagicMock(
            return_value=expectedresult)
        fetch_service.store_health_centers()

        health_service_loc = fetch_service.fetch_health_center_informations()

        assert health_service_loc[0]["center_name"] == "Balbriggan Health Centre"
        assert health_service_loc[0]["center_address"] == "Hampton Street,Balbriggan,Co. Dublinend"
        assert health_service_loc[0]["center_phone"] == "+353 1 8834906"
        self.assertAlmostEqual(
            health_service_loc[0]["center_lat"], 0.786, None, None, 0.002)
        self.assertAlmostEqual(
            health_service_loc[0]["center_lon"], -0.156, None, None, 0.002)

    # Testing gardastation functions over database.
    def test_read_garda_stations(self):
        read_services = StoreServiceData()
        assert read_services.read_garda_stations()[0] == ['Name', 'Address1', 'Address2', 'Address3', 'Phone', 'Website', 'Division',
                                                          'Divisional_HQ', 'Divisional_HQ_Phone', 'District', 'District_HQ', 'District_HQ_Phone', 'Opening_Hours', 'LAT', 'LONG']
        assert read_services.read_garda_stations(
        )[1][0] == "Balbriggan Garda Station"

    def test_store_garda_stations(self):
        store_service = StoreServiceData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ['Balbriggan Garda Station', 'Drogheda Road,', 'Balbriggan,', 'Co. Dublin,', '+353 1 8020510', ' http://www.garda.ie/Stations/Default.aspx',
                               'Dublin Metropolitan Region Northern Division', 'Ballymun', '+353 1 6664493', 'Balbriggan', 'Balbriggan', '+353 1 8020510', 'Open 24hrs', 0.78656, -0.1563]]

        store_service.read_garda_stations = MagicMock(
            return_value=expectedresult)
        store_service.store_garda_stations()

        fetch_garda_station = GardaStations.objects(
            station="Balbriggan Garda Station").first()
        assert fetch_garda_station["station_address"] == "Drogheda Road,Balbriggan,Co. Dublin,"
        assert fetch_garda_station["station_division"] == "Dublin Metropolitan Region Northern Division"
        assert fetch_garda_station["station_divisional_hq"] == "Ballymun"
        assert fetch_garda_station["station_phone"] == "+353 1 8020510"
        self.assertAlmostEqual(
            fetch_garda_station["station_lat"], Decimal(0.786), None, None, 0.001)
        self.assertAlmostEqual(
            fetch_garda_station["station_lon"], Decimal(-0.156), None, None, 0.001)

    def test_fetch_garda_station_informations(self):
        fetch_service_garda = StoreServiceData()

        expectedresult = [[], ['Balbriggan Garda Station', 'Drogheda Road,', 'Balbriggan,', 'Co. Dublin,', '+353 1 8020510', ' http://www.garda.ie/Stations/Default.aspx',
                               'Dublin Metropolitan Region Northern Division', 'Ballymun', '+353 1 6664493', 'Balbriggan', 'Balbriggan', '+353 1 8020510', 'Open 24hrs', 0.78656, -0.1563]]
        fetch_service_garda.read_garda_stations = MagicMock(
            return_value=expectedresult)
        fetch_service_garda.store_garda_stations()

        garda_service_loc = fetch_service_garda.fetch_garda_station_informations()

        assert garda_service_loc[0]["station_address"] == "Drogheda Road,Balbriggan,Co. Dublin,"
        assert garda_service_loc[0]["station_division"] == "Dublin Metropolitan Region Northern Division"
        assert garda_service_loc[0]["station_divisional_hq"] == "Ballymun"
        assert garda_service_loc[0]["station_phone"] == "+353 1 8020510"
        self.assertAlmostEqual(
            garda_service_loc[0]["station_lat"], 0.786, None, None, 0.002)
        self.assertAlmostEqual(
            garda_service_loc[0]["station_lon"], -0.156, None, None, 0.002)

    # Testing hospital functions over database.
    def test_read_hospitals(self):
        read_services = StoreServiceData()
        assert read_services.read_hospitals()[0] == [
            'name', 'address', 'eircode', 'x', 'y']
        assert read_services.read_hospitals(
        )[1][0] == "Midland Regional Hospital Portlaoise"

    def test_store_hospitals(self):
        store_service = StoreServiceData()
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ["Midland Regional Hospital Portlaoise",
                               "Dublin Road, Portlaoise, Co. Laois, ", "yyy", 0.78656, -0.1563]]

        store_service.read_hospitals = MagicMock(
            return_value=expectedresult)
        store_service.store_hospitals()

        fetch_hospital_service = Hospitals.objects(
            center_name="Midland Regional Hospital Portlaoise").first()

        assert fetch_hospital_service["center_address"] == "Dublin Road, Portlaoise, Co. Laois, "
        self.assertAlmostEqual(
            fetch_hospital_service["center_lat"], Decimal(0.786), None, None, 0.001)
        self.assertAlmostEqual(
            fetch_hospital_service["center_lon"], Decimal(-0.156), None, None, 0.001)

    def test_fetch_hospital_informations(self):
        fetch_service = StoreServiceData()
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        expectedresult = [[], ["Midland Regional Hospital Portlaoise",
                               "Dublin Road, Portlaoise, Co. Laois, ", "yyy", 0.78656, -0.1563]]
        fetch_service.read_hospitals = MagicMock(
            return_value=expectedresult)
        fetch_service.store_hospitals()

        hospital_service_loc = fetch_service.fetch_hospital_informations()
        assert hospital_service_loc[0]["center_name"] == "Midland Regional Hospital Portlaoise"
        assert hospital_service_loc[0]["center_address"] == "Dublin Road, Portlaoise, Co. Laois, "
        self.assertAlmostEqual(
            hospital_service_loc[0]["center_lat"], 0.786, None, None, 0.002)
        self.assertAlmostEqual(
            hospital_service_loc[0]["center_lon"], -0.156, None, None, 0.002)
