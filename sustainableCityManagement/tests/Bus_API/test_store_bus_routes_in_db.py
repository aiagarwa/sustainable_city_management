import pandas as pd
from datetime import datetime, timedelta, date
from django.test import TestCase
from unittest.mock import MagicMock
from main_project.Bus_API.store_bus_routes_data_in_database import StoreBusRoutesData
from main_project.Bus_API.bus_collections_db import BusStops, BusTimings, BusRoutes, BusTrips, BusPath
from mongoengine import *
import mongomock as mm
from decimal import Decimal


class TestStoreBusRoutesData(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_read_bus_stops(self):
        read_bus_stops = StoreBusRoutesData()
        assert read_bus_stops.read_bus_stops()[0] == [
            '\ufeffstop_id', 'stop_name', 'stop_lat', 'stop_lon']
        assert read_bus_stops.read_bus_stops()[1][1] == "Killeen Bridge"

    def test_store_bus_stops(self):
        store_bus_stops_loc = StoreBusRoutesData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ["35", "Dublin Bus Stop2", 0.78656, -0.1563]]

        store_bus_stops_loc.read_bus_stops = MagicMock(
            return_value=expectedresult)
        store_bus_stops_loc.store_bus_stops()

        fetch_bus_stops = BusStops.objects(
            stop_name="Dublin Bus Stop2").first()

        assert fetch_bus_stops["stop_name"] == "Dublin Bus Stop2"
        assert fetch_bus_stops["stop_id"] == "35"
        self.assertAlmostEqual(
            fetch_bus_stops["stop_lat"], Decimal(0.786), None, None, 0.001)
        self.assertAlmostEqual(
            fetch_bus_stops["stop_lon"], Decimal(-0.156), None, None, 0.001)

    def test_fetch_busstops_location(self):
        fetch_bus_stops_loc = StoreBusRoutesData()
        expectedresult = [[], ["35", "Dublin Bus Stop2", 0.78656, -0.1563]]

        fetch_bus_stops_loc.read_bus_stops = MagicMock(
            return_value=expectedresult)
        fetch_bus_stops_loc.store_bus_stops()

        bus_stops_loc = fetch_bus_stops_loc.fetch_busstops_location()

        assert bus_stops_loc[0]["stop_name"] == "Dublin Bus Stop2"
        assert bus_stops_loc[0]["stop_id"] == "35"
        self.assertAlmostEqual(
            bus_stops_loc[0]["stop_lat"], 0.786, None, None, 0.002)
        self.assertAlmostEqual(
            bus_stops_loc[0]["stop_lon"], -0.156, None, None, 0.002)

    def test_read_bus_routes(self):
        read_bus_routes = StoreBusRoutesData()
        assert read_bus_routes.read_bus_routes()[0] == [
            '\ufeffroute_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_type']
        assert read_bus_routes.read_bus_routes()[1][0] == "10-100-e19-1"

    def test_store_bus_routes(self):
        store_bus_stops_routes = StoreBusRoutesData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ["566-45-e41", 78, 'BR1', "Bus Route 1"]]

        store_bus_stops_routes.read_bus_routes = MagicMock(
            return_value=expectedresult)
        store_bus_stops_routes.store_bus_routes()

        fetch_bus_routes = BusRoutes.objects().first()

        assert fetch_bus_routes["route_name"] == "Bus Route 1"
        assert fetch_bus_routes["route_id"] == "566-45-e41"

    def test_fetch_busroutes(self):
        fetch_bus_routes = StoreBusRoutesData()
        expectedresult = [[], ["566-45-e41", 78, 'BR1', "Bus Route 1"]]

        fetch_bus_routes.read_bus_routes = MagicMock(
            return_value=expectedresult)
        fetch_bus_routes.store_bus_routes()

        bus_routes = fetch_bus_routes.fetch_busroutes()

        assert bus_routes[0]["route_name"] == "Bus Route 1"
        assert bus_routes[0]["route_id"] == "566-45-e41"

    def test_read_bus_trips(self):
        read_bus_trip = StoreBusRoutesData()
        assert read_bus_trip.read_bus_trips()[0] == [
            'route_id', 'service_id', 'trip_id', 'shape_id', 'trip_headsign', 'direction_id']
        assert read_bus_trip.read_bus_trips()[1][2] == "1381339.3.10-101-e19-1.261.I"

    def test_store_bus_trips(self):
        store_bus_trips = StoreBusRoutesData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ["17-e19-34", "tyy",
                               "345.3.I", "1345.3.I", "Bus Station 1", "1"]]

        store_bus_trips.read_bus_trips = MagicMock(return_value=expectedresult)
        store_bus_trips.store_bus_trips()

        fetch_bus_trips = BusTrips.objects().first()

        assert fetch_bus_trips["trip_id"] == "345.3.I"
        assert fetch_bus_trips["route_id"] == "17-e19-34"

    def test_store_bus_times(self):
        store_bus_trips = StoreBusRoutesData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ["17-e19-34", "tyy",
                               "345.3.I", "1345.3.I", "Bus Station 1", "1"]]

        store_bus_trips.read_bus_trips = MagicMock(return_value=expectedresult)
        store_bus_trips.store_bus_trips()

        expectedresult_timings_df = pd.DataFrame({'trip_id': ["345.3.I", "345.3.I"], 'arrival_time': ["06:20:00", "06:25:00"], 'departure_time': [
                                                 "06:20:00", "06:25:00"], 'stop_id': ["7866R56", "7866RT7"], 'stop_sequence': [1, 2]})
        store_bus_trips.pd.read_csv = MagicMock(
            return_value=expectedresult_timings_df)
        store_bus_trips.store_bus_times()

        fetch_bus_trips = BusTrips.objects().first()
        
        assert fetch_bus_trips["trip_id"] == "345.3.I"
        assert fetch_bus_trips["stops"][0]["stop_id"] == "7866R56"
        assert fetch_bus_trips["stops"][0]["stop_arrival_time"] == "06:20:00"
        assert fetch_bus_trips["stops"][0]["stop_departure_time"] == "06:20:00"
        assert fetch_bus_trips["stops"][0]["stop_sequence"] == 1

    def test_fetch_bustrips(self):
        fetch_bus_trips = StoreBusRoutesData()

        expectedresult = [[], ["17-e19-34", "tyy",
                               "345.3.I", "1345.3.I", "Bus Station 1", "1"]]

        fetch_bus_trips.read_bus_trips = MagicMock(return_value=expectedresult)
        fetch_bus_trips.store_bus_trips()

        expectedresult_timings_df = pd.DataFrame({'trip_id': ["345.3.I", "345.3.I"], 'arrival_time': ["06:20:00", "06:25:00"], 'departure_time': [
                                                 "06:20:00", "06:25:00"], 'stop_id': ["7866R56", "7866RT7"], 'stop_sequence': [1, 2]})
        fetch_bus_trips.pd.read_csv = MagicMock(
            return_value=expectedresult_timings_df)
        fetch_bus_trips.store_bus_times()

        bus_trips = fetch_bus_trips.fetch_bustrips()

        assert bus_trips[0]["trip_id"] == "345.3.I"
        assert bus_trips[0]["stops"][0]["stop_id"] == "7866R56"
        assert bus_trips[0]["stops"][0]["stop_arrival_time"] == "06:20:00"
        assert bus_trips[0]["stops"][0]["stop_departure_time"] == "06:20:00"
        assert bus_trips[0]["stops"][0]["stop_sequence"] == 1

    def test_read_bus_paths(self):
        read_bus_stops = StoreBusRoutesData()
        first_datapoint = read_bus_stops.read_bus_paths()['paths'][0]

        assert first_datapoint['start'] == '8300B1359501'
        assert first_datapoint['end'] == '8300B1006201'
        assert first_datapoint['coordinates'][0] == [53.711935, -6.352762]

    def test_store_bus_paths(self):
        store_bus_stops_loc = StoreBusRoutesData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = {
            "paths": [
                {
                "start": "8300B1359501",
                "end": "8300B1006201",
                "coordinates": [
                    [53.711935, -6.352762]
                ]
                }
            ]
        }

        store_bus_stops_loc.read_bus_paths = MagicMock(
            return_value=expectedresult)
        store_bus_stops_loc.store_bus_paths()

        bus_path= BusPath.objects(
            _id='8300B13595018300B1006201').first()

        assert bus_path["start_stop_id"] == "8300B1359501"
        assert bus_path["end_stop_id"] == "8300B1006201"
        self.assertAlmostEqual(
            bus_path.coordinates[0]['lat'], Decimal(53.711935), None, None, 0.001)
        self.assertAlmostEqual(
            bus_path.coordinates[0]['lon'], Decimal(-6.352762), None, None, 0.001)

    def test_fetch_bus_paths(self):
        fetch_bus_stops_loc = StoreBusRoutesData()

        expectedresult = {
            "paths": [
                {
                "start": "8300B1359501",
                "end": "8300B1006201",
                "coordinates": [
                    [53.711935, -6.352762]
                ]
                }
            ]
        }

        fetch_bus_stops_loc.read_bus_paths = MagicMock(
            return_value=expectedresult)
        fetch_bus_stops_loc.store_bus_paths()

        bus_paths = fetch_bus_stops_loc.fetch_bus_paths()

        assert bus_paths == [
            {
                '_id': '8300B13595018300B1006201',
                'start_stop_id': '8300B1359501',
                'end_stop_id': '8300B1006201',
                'coordinates': [
                    {
                        'lat': 53.711935,
                        'lon': -6.352762
                    }
                ]
            }
        ]

