from main_project.Footfall_API.store_footfall_data_in_database import StoreFootfallData
from main_project.Footfall_API.footfall_collections_db import FootfallDateBased, FootfallInfo, FootfallOverall
from django.test import TestCase
from unittest.mock import MagicMock
from decimal import Decimal
import mongomock as mm
from mongoengine import get_connection
from main_project.Config.config_handler import read_config
import json
import mock
from datetime import datetime
import pandas as pd
import numpy as np
import requests
from freezegun import freeze_time
from freezegun.api import FakeDatetime
from pandas.util.testing import assert_frame_equal


@freeze_time("2021-03-20 15:15:15")
class TestStoreFootfalldataToDatabase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def tearDown(self):
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        FootfallDateBased.objects().delete()
        FootfallOverall.objects().delete()

    def test_calculate_average_footfall_overall(self):
        calculate_fn = StoreFootfallData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        mocked_input = pd.DataFrame(np.array([[0, 1, 2, 3], [0, 4, 5, 6], [0, 7, 8, 9]]),
                                    columns=['Time', 'Place_1', 'Place_2', 'Place_3'])
        calculate_fn.read_footfall = MagicMock(return_value=mocked_input)

        result = calculate_fn.calculate_average_footfall_overall()

        expected_result = {'Place_1': 4, 'Place_2': 5, 'Place_3': 6}
        assert result == expected_result

    def test_calculate_average_footfall_date_based(self):
        calculate_fn = StoreFootfallData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        data = [['20-03-2021 15:15:15', 1, 2, 3], ['20-03-2021 15:15:15', 4, 5, 6],
                ['21-03-2021 15:15:15', 7, 8, 9], ['21-03-2021 15:15:15', 7, 8, 9]]
        mocked_input1 = pd.DataFrame(
            data, columns=['Time', 'Place1', 'Place2', 'Place3'])
        calculate_fn.read_footfall = MagicMock(return_value=mocked_input1)

        result_date = calculate_fn.calculate_average_footfall_date_based()
        expected_result = {'Place1': {'2021-03-20': 2, '2021-03-21': 7}, 'Place2': {
            '2021-03-20': 3, '2021-03-21': 8}, 'Place3': {'2021-03-20': 4, '2021-03-21': 9}}
        assert result_date == expected_result

    def test_store_footfall_overall(self):
        store_fn = StoreFootfallData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        mocked_input = {'Place_1': 4, 'Place_2': 5, 'Place_3': 6}
        store_fn.calculate_average_footfall_overall = MagicMock(
            return_value=mocked_input)
        store_fn.store_footfall_overall()
        fetch_footfall_overall = FootfallOverall.objects(
            location="Place_1").first()
        assert fetch_footfall_overall["count"] == 4

    def test_store_footfall_locations(self):
        store_fn_location = StoreFootfallData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        mocked_input = {'Place_1': 4, 'Place_2': 5, 'Place_3': 6}
        store_fn_location.calculate_average_footfall_overall = MagicMock(
            return_value=mocked_input)

        store_fn_location.store_footfall_locations()
        fetch_footfall_location = FootfallDateBased.objects().first()
        assert fetch_footfall_location["location"] == 'Place_1'

    def test_store_footfall_data_datebased(self):
        store_fn_datebased = StoreFootfallData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        mocked_input = {'Place_1': {'2021-03-20': 2, '2021-03-21': 7}, 'Place_2': {
            '2021-03-20': 3, '2021-03-21': 8}, 'Place_3': {'2021-03-20': 4, '2021-03-21': 9}}
        store_fn_datebased.calculate_average_footfall_date_based = MagicMock(
            return_value=mocked_input)
        self.test_store_footfall_locations()
        store_fn_datebased.store_footfall_data_datebased()
        fetch_footfall_date = FootfallDateBased.objects(
            location="Place_1").first()
        assert str(
            fetch_footfall_date.footfall_data[0].data_date) == '2021-03-20 00:00:00'
        assert fetch_footfall_date.footfall_data[0].count == 2

    def test_fetch_data_from_db_for_day(self):
        fetch_fn_datebased = StoreFootfallData()
        start = '2021-03-20'
        end = '2021-03-20'
        conn = get_connection()
        self.test_store_footfall_data_datebased()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        fetch_fn_datebased.fetch_data_from_db_for_day(start, end)
        result_1 = expected_result = [{'location': 'Place_1', 'footfall_data': [{'data_date': FakeDatetime(2021, 3, 20, 0, 0), 'count': 2}]}, {'location': 'Place_2', 'footfall_data': [
            {'data_date': FakeDatetime(2021, 3, 20, 0, 0), 'count': 3}]}, {'location': 'Place_3', 'footfall_data': [{'data_date': FakeDatetime(2021, 3, 20, 0, 0), 'count': 4}]}]
        assert expected_result == result_1

    def test_fetch_footfall_overall(self):
        fetch_fn_overall = StoreFootfallData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        self.test_store_footfall_overall()
        result_all = fetch_fn_overall.fetch_footfall_overall()
        assert result_all[0]['location'] == 'Place_1'
        assert result_all[0]['count'] == 4

    def test_get_last_date(self):
        date_fn_overall = StoreFootfallData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        self.test_store_footfall_data_datebased()
        date = date_fn_overall.get_last_date('Place_1')
        print(date)
        assert str(date) == '2021-03-21'

    def test_fetch_data_from_db_with_prediction(self):
        predict_fn_overall = StoreFootfallData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))
        self.test_store_footfall_data_datebased()
        days_interval = 2
        reqd_location = 'Place_1'
        result, date = predict_fn_overall.fetch_data_from_db_with_prediction(
            days_interval, reqd_location)
        assert result == [{'location': 'Place_1', 'footfall_data': [{'data_date': FakeDatetime(
            2021, 3, 20, 0, 0), 'count': 2}, {'data_date': FakeDatetime(2021, 3, 21, 0, 0), 'count': 7}]}]
        assert str(date) == '2021-03-21 00:00:00'
