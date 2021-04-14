from main_project.ML_models.footfall_prediction import *
from django.test import TestCase
from unittest.mock import MagicMock
from main_project.Config.config_handler import read_config
import datetime
import unittest


class TestFootfallUsagePrediction(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    # Testing the prediction function works for given input array of data.

    def test_predict_footfall_usage(self):
        arrayOfUsagePerDay = [10, 20, 30, 45, 12, 16,
                              30, 15, 10, 20, 35, 15, 10, 20, 37, 15, 10, 20, 39, 15, 15, 20, 30, 15]
        result = predict_footfall(arrayOfUsagePerDay, predictDays=1,
                                  previous_days_to_consider=config_vals["days_to_consider_for_prediction"])
        expected_result = 22
        assert (expected_result == result)
