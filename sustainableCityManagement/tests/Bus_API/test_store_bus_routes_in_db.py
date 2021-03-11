from django.test import TestCase
from unittest.mock import MagicMock
from main_project.Bus_API.store_bus_routes_data_in_database import StoreBusRoutesData
from main_project.Bus_API.store_bus_routes_data_in_database import BusStops
from mongoengine import *
from mongoengine.queryset import queryset_manager
from decimal import Decimal
import json

class BaseDocument(Document):
    meta = {'abstract': True}
    
    @queryset_manager
    def query(self, queryset):
        return queryset

class TestBusStop(BaseDocument):
    stop_name = StringField(max_length=200)
    stop_id = StringField(max_length=200, unique=True)
    stop_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    stop_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')

class TestStoreBusRoutesData(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_read_bus_stops(self):
        read_bus_stops = StoreBusRoutesData()
        assert read_bus_stops.read_bus_stops()[0]==['\ufeffstop_id','stop_name','stop_lat','stop_lon']
        assert read_bus_stops.read_bus_stops()[1][1]=="Killeen Bridge"

    def test_store_bus_stops(self):
        store_bus_stops_loc = StoreBusRoutesData()
        expectedresult =  [[],["35", "Dublin Bus Stop2", 0.78656, -0.1563]]

        store_bus_stops_loc.read_bus_stops = MagicMock(return_value=expectedresult)
        store_bus_stops_loc.store_bus_stops()        

        fetch_bus_stops = BusStops.objects(stop_name="Dublin Bus Stop2").first()

        assert fetch_bus_stops["stop_name"] == "Dublin Bus Stop2"
        assert fetch_bus_stops["stop_id"] == "35"
        self.assertAlmostEqual(fetch_bus_stops["stop_lat"],Decimal(0.786),None,None,0.001)
        self.assertAlmostEqual(fetch_bus_stops["stop_lon"],Decimal(-0.156),None,None,0.001)

        BusStops.objects(stop_name="Dublin Bus Stop2").delete()

