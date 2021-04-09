from main_project.Footfall_API import fetch_footfallapi
from main_project.Footfall_API.footfall_collections_db import FootfallOverall, FootfallInfo, FootfallDateBased
from main_project.Footfall_API.store_footfall_data_in_database import StoreFootfallData
from main_project.Config.config_handler import read_config
from django.test import TestCase
from unittest.mock import MagicMock
from mock import patch
import mongomock as mm
from mongoengine import get_connection
import json
import datetime
from freezegun import freeze_time

config_vals = read_config("Footfall_API")


@freeze_time("2021-03-20 17")
class TestFetchFootfallApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def tearDown(self):
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        FootfallDateBased.objects().delete()
        FootfallOverall.objects().delete()

    def test_footfall_datebased_graphvalues_predictions(self):
        fetch_graph_value = fetch_footfallapi.FootfallApi()
        FootfallDateBased(location='Place_3').save()
        footfall_2 = FootfallDateBased.objects(location='Place_3').first()
        for i in range(20):
            footfall_2.footfall_data.append(FootfallInfo(
                data_date='2021-03-20 13:15:15', count=i))
            footfall_2.save()
        footfall_2.footfall_data.append(FootfallInfo(
            data_date='2021-03-21 13:15:15', count=5))
        footfall_2.save()
        result = fetch_graph_value.footfall_datebased_graphvalues_predictions(
            'Place_3', days_interval=config_vals["days_interval_size"])
        expected_result = {'Place_3': {'2021-03-20': 19, '2021-03-22': 20}}
        assert result == expected_result

    def test_footfall_overall(self):
        FootfallOverall(location="Aston Quay", count="5").save()
        fetch_location = fetch_footfallapi.FootfallApi()
        result = fetch_location.footfall_overall()
        expected_result = {'Aston Quay': {'Footfall': 5,
                                          'Lat': 53.3467400813258, 'Lon': -6.260702178407169}}
        assert result == expected_result
