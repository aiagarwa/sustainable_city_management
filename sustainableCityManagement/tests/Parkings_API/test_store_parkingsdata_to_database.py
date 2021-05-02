from main_project.Parkings_API.store_parkingsdata_to_database import StoreParkingsData
from main_project.Parkings_API.parkings_collections_db import ParkingAvailability, ParkingsAvailability
from django.test import TestCase
from unittest.mock import MagicMock
import xml.etree.ElementTree as ET
from decimal import Decimal
import mongomock as mm
from mongoengine import get_connection
from main_project.Config.config_handler import read_config
import json
import mock
from datetime import datetime
import requests
from freezegun import freeze_time
from freezegun.api import FakeDatetime

config_vals = read_config("Parkings_API")


@freeze_time("2021-03-15 15:15:15")
class TestStoreParkingsData(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def tearDown(self):
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        ParkingsAvailability.objects().delete()

    def test_get_parkings_spaces_availability_live(self):
        fetch_Parkings_to_database = StoreParkingsData()
        status = fetch_Parkings_to_database.get_parkings_spaces_availability_live()
        assert status != None

    def test_save_parkings_data(self):
        store_Parkings_to_database = StoreParkingsData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        Mocked_result = """<?xml version="1.0" encoding="ISO-8859-1"?>
        <carparkData>
            <Northwest>
            <carpark name="PARNELL" spaces="302"> </carpark>
            </Northwest>
        <Timestamp>08:34:13 on Wednesday 14/03/2021</Timestamp>
        </carparkData>"""
        Mocked_result = ET.fromstring(Mocked_result)
        store_Parkings_to_database.get_parkings_spaces_availability_live = MagicMock(
            return_value=Mocked_result)
        store_Parkings_to_database.store_parking_spaces_availability_live()

        fetch_parkings_data = ParkingsAvailability.objects(
            updateTimestamp="08:34:13 on Wednesday 14/03/2021").first()
        assert fetch_parkings_data.parkings[0]["area"] == "NORTHWEST"
        assert fetch_parkings_data.parkings[0]["name"] == "PARNELL"
        assert fetch_parkings_data.parkings[0]["availableSpaces"] == 302

    def test_fetch_data_from_db_for_day(self):
        fetch_Parkings_from_database_day = StoreParkingsData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        self.test_save_parkings_data()
        date = "2021-03-14"
        startdate = datetime.strptime(date, "%Y-%m-%d")
        result = fetch_Parkings_from_database_day.fetch_data_from_db_for_day(
            startdate)
        assert str(result[0]["updateTimestamp"]) == "2021-03-14 08:34:13"

    def test_fetch_data_from_db_historical(self):
        fetch_Parkings_from_database_hist = StoreParkingsData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        self.test_save_parkings_data()
        ParkingsAvailability(updateTimestamp='2021-03-14 09:34:13').save()
        ParkingsAvailability(updateTimestamp='2021-03-13 08:34:13').save()

        Parkings_1 = ParkingsAvailability.objects(
            updateTimestamp='2021-03-14 09:34:13').first()
        Parkings_2 = ParkingsAvailability.objects(
            updateTimestamp='2021-03-13 08:34:13').first()

        Parkings_1.parkings.append(
            ParkingAvailability(
                area="NORTHWEST",
                name="PARNELL",
                availableSpaces=50)
        )
        Parkings_1.save()

        Parkings_2.parkings.append(
            ParkingAvailability(
                area="NORTHWEST",
                name="PARNELL",
                availableSpaces=60)
        )
        Parkings_2.save()
        startdate = "2021-03-12"
        startdate = datetime.strptime(startdate, "%Y-%m-%d")
        enddate = "2021-03-15"
        enddate = datetime.strptime(enddate, "%Y-%m-%d")
        result = fetch_Parkings_from_database_hist.fetch_data_from_db_historical(
            startdate, enddate)
        assert result[0]["parkings"]["PARNELL"] == 60
        assert result[1]["parkings"]["PARNELL"] == 176

    def test_daterange(self):
        fetch_Parkings_date = StoreParkingsData()
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        startdate = "2021-03-14"
        startdate = datetime.strptime(startdate, "%Y-%m-%d")
        enddate = "2021-03-15"
        enddate = datetime.strptime(enddate, "%Y-%m-%d")
        result = fetch_Parkings_date.daterange(startdate, enddate)
        for items in result:
            if (str(items) != "2021-03-14 00:00:00"):
                assert str(items) == "2021-03-15 00:00:00"
