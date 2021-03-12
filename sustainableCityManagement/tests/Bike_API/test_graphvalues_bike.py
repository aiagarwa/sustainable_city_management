from main_project.Bike_API.graphvalues_bike import GraphValuesBike
from django.test import TestCase
from unittest.mock import MagicMock
from freezegun import freeze_time

class TestGraphValuesBike(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_graphvalue_call_overall_returns_error_with_days_historical_0(self):
        graph_values_bike = GraphValuesBike()

        with self.assertRaises(ValueError) as context:
            graph_values_bike.graphvalue_call_overall(days_historical=0)
        assert str(context.exception) == 'Assign days_historic parameter >= 2.'

    def test_graphvalue_call_overall_returns_error_with_days_historical_1(self):
        graph_values_bike = GraphValuesBike()

        with self.assertRaises(ValueError) as context:
            graph_values_bike.graphvalue_call_overall(days_historical=1)
        assert str(context.exception) == 'Assign days_historic parameter >= 2.'
