from django.test import TestCase
from unittest.mock import MagicMock
from main_project.Bus_API.store_bus_routes_data_in_database import StoreBusRoutesData

class TestStoreBusRoutesData(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_read_bus_stops(self):
        read_bus_stops = StoreBusRoutesData()
        assert read_bus_stops.read_bus_stops()[0]==['\ufeffstop_id','stop_name','stop_lat','stop_lon']
        assert read_bus_stops.read_bus_stops()[1][1]=="Killeen Bridge"
        


