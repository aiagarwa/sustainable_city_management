from main_project.ML_models.bikes_usage_prediction import *
from django.test import TestCase
from unittest.mock import MagicMock
from main_project.Config.config_handler import read_config
import datetime
import unittest


class TestBikeUsagePrediction(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    # Testing the prediction function works for given input array of data.

    def test_predict_bikes_usage(self):
        arrayOfUsagePerDay = [10, 20, 30, 15]
        result = predict_bikes_usage(arrayOfUsagePerDay, predictDays=1,
                                     previous_days_to_consider=config_vals["days_to_consider_for_prediction"])
        expected_result = 23
        assert (expected_result == result)
