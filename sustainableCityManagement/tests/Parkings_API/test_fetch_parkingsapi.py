from main_project.Parkings_API.fetch_parkingsapi import FetchParkingsApi
from main_project.Parkings_API.store_parkingsdata_to_database import StoreParkingsData
from main_project.Parkings_API.parkings_collections_db import ParkingAvailability, ParkingsAvailability
from django.test import TestCase
from unittest.mock import MagicMock
from mock import patch
import json
from datetime import datetime
import mongomock as mm
from mongoengine import get_connection
from freezegun import freeze_time
from freezegun.api import FakeDatetime


@freeze_time("2021-03-11 17")
class TestFetchParkingsApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def tearDown(self):
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        ParkingsAvailability.objects().delete()

    def test_parkings_availability(self):
        fetch_parkings_availability = FetchParkingsApi()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
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
        enddate = "2021-03-15"
        mocked_result = [{'_id': {'$oid': None}, 'updateTimestamp': {'$date': FakeDatetime(2021, 3, 13, 0, 0)}, 'parkings': {'PARNELL': 60}}, {
            '_id': {'$oid': None}, 'updateTimestamp': {'$date': FakeDatetime(2021, 3, 14, 0, 0)}, 'parkings': {'PARNELL': 50}}]

        result = fetch_parkings_availability.parkings_availability(
            startdate, enddate)

        assert result == mocked_result
