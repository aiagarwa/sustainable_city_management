import pandas as pd
from datetime import datetime, timedelta, date
from django.test import TestCase
from unittest.mock import MagicMock
from main_project.Parkings_Recreational_Places_API.store_recreational_locations_in_db import StoreRecreationalPlacesParkingsData
from main_project.Parkings_Recreational_Places_API.recreational_places_parkings_collections_db import Parks, Beaches, PlayingPitches, Cinemas
from mongoengine import *
import mongomock as mm
from decimal import Decimal


class TestStoreRecreationalPlacesData(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_read_beaches_locations(self):
        read_beaches_locations = StoreRecreationalPlacesParkingsData()
        assert read_beaches_locations.read_beaches_locations()[0] == [
            'ID', 'NAME', 'LAT', 'LONG']
        assert read_beaches_locations.read_beaches_locations()[1][1] == "Loughshinny"

    def test_store_beaches_locations(self):
        store_beaches_loc = StoreRecreationalPlacesParkingsData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], [35, "Dublin Beach", 0.23656, -0.1963]]

        store_beaches_loc.read_beaches_locations = MagicMock(
            return_value=expectedresult)
        store_beaches_loc.store_beaches_locations()

        fetch_beaches_locations = Beaches.objects(
            beach_name="Dublin Beach").first()

        assert fetch_beaches_locations["beach_name"] == "Dublin Beach"
        assert fetch_beaches_locations["beach_id"] == 35
        self.assertAlmostEqual(
            fetch_beaches_locations["beach_lat"], Decimal(0.236), None, None, 0.005)
        self.assertAlmostEqual(
            fetch_beaches_locations["beach_lon"], Decimal(-0.196), None, None, 0.005)

    def test_fetch_beaches_location(self):
        fetch_beaches_loc = StoreRecreationalPlacesParkingsData()
        expectedresult = [[], [35, "Dublin Beach", 0.23656, -0.1963]]

        fetch_beaches_loc.read_beaches_locations = MagicMock(
            return_value=expectedresult)
        fetch_beaches_loc.store_beaches_locations()

        beaches_loc = fetch_beaches_loc.fetch_beaches_location()

        assert beaches_loc[0]["beach_name"] == "Dublin Beach"
        assert beaches_loc[0]["beach_id"] == 35
        self.assertAlmostEqual(
            beaches_loc[0]["beach_lat"], 0.236, None, None, 0.005)
        self.assertAlmostEqual(
            beaches_loc[0]["beach_lon"], -0.196, None, None, 0.005)

    def test_read_playing_pitches_locations(self):
        read_playing_pitches = StoreRecreationalPlacesParkingsData()
        assert read_playing_pitches.read_playing_pitches_locations()[0] == [
            'FACILITY_TYPE', 'FACILITY_NAME','LOCATION', 'LAT', 'LONG']
        assert read_playing_pitches.read_playing_pitches_locations()[1][1] == "Balbriggan Town Park"

    def test_store_playing_pitches(self):
        store_playing_pitches_loc = StoreRecreationalPlacesParkingsData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ["Basketball Court", "Facility_BB","Dublin",0.23656, -0.1963]]

        store_playing_pitches_loc.read_playing_pitches_locations = MagicMock(
            return_value=expectedresult)
        store_playing_pitches_loc.store_playing_pitches_locations()

        fetch_playing_pitches_locations = PlayingPitches.objects(
            facility_name="Facility_BB").first()

        assert fetch_playing_pitches_locations["facility_name"] == "Facility_BB"
        assert fetch_playing_pitches_locations["facility_type"] == "Basketball Court"
        assert fetch_playing_pitches_locations["facility_location"] == "Dublin"
        self.assertAlmostEqual(
            fetch_playing_pitches_locations["facility_lat"], Decimal(0.236), None, None, 0.005)
        self.assertAlmostEqual(
            fetch_playing_pitches_locations["facility_lon"], Decimal(-0.196), None, None, 0.005)

    def test_fetch_playing_pitches_location(self):
        fetch_playing_pitches_loc = StoreRecreationalPlacesParkingsData()
        expectedresult = [[], ["Basketball Court", "Facility_BB","Dublin",0.23656, -0.1963]]

        fetch_playing_pitches_loc.read_playing_pitches_locations = MagicMock(
            return_value=expectedresult)
        fetch_playing_pitches_loc.store_playing_pitches_locations()

        playing_pitches_loc = fetch_playing_pitches_loc.fetch_playing_pitches_location()

        assert playing_pitches_loc[0]["facility_name"] == "Facility_BB"
        assert playing_pitches_loc[0]["facility_type"] == "Basketball Court"
        assert playing_pitches_loc[0]["facility_location"] == "Dublin"
        self.assertAlmostEqual(
            playing_pitches_loc[0]["facility_lat"], 0.236, None, None, 0.005)
        self.assertAlmostEqual(
            playing_pitches_loc[0]["facility_lon"], -0.196, None, None, 0.005)

    def test_read_parks_locations(self):
        read_parks = StoreRecreationalPlacesParkingsData()
        assert read_parks.read_parks_locations()[0] == [
            'Name', 'Address','Area', 'LAT', 'LONG']
        assert read_parks.read_parks_locations()[1][0] == "Ardgillan Demesne"

    def test_store_parks(self):
        store_parks_loc = StoreRecreationalPlacesParkingsData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ["Dublin Park", "Co. Dublin",770262.7877,0.23656, -0.1963]]

        store_parks_loc.read_parks_locations = MagicMock(return_value=expectedresult)
        store_parks_loc.store_parks_locations()

        fetch_parks_locations = Parks.objects(park_name="Dublin Park").first()

        assert fetch_parks_locations["park_name"] == "Dublin Park"
        assert fetch_parks_locations["park_address"] == "Co. Dublin"
        self.assertAlmostEqual(
            fetch_parks_locations["park_area"], Decimal(770262.787), None, None, 0.005)
        self.assertAlmostEqual(
            fetch_parks_locations["park_lat"], Decimal(0.236), None, None, 0.005)
        self.assertAlmostEqual(
            fetch_parks_locations["park_lon"], Decimal(-0.196), None, None, 0.005)

    def test_fetch_parks_location(self):
        fetch_parks_loc = StoreRecreationalPlacesParkingsData()
        expectedresult = [[], ["Dublin Park", "Co. Dublin",770262.7877,0.23656, -0.1963]]

        fetch_parks_loc.read_parks_locations = MagicMock(
            return_value=expectedresult)
        fetch_parks_loc.store_parks_locations()

        parks_loc = fetch_parks_loc.fetch_parks_location()

        assert parks_loc[0]["park_name"] == "Dublin Park"
        assert parks_loc[0]["park_address"] == "Co. Dublin"
        self.assertAlmostEqual(
            parks_loc[0]["park_area"], 770262.787, None, None, 0.005)
        self.assertAlmostEqual(
            parks_loc[0]["park_lat"], 0.236, None, None, 0.005)
        self.assertAlmostEqual(
            parks_loc[0]["park_lon"], -0.196, None, None, 0.005)

    def test_read_cinemas_locations(self):
        read_cinemas_locations = StoreRecreationalPlacesParkingsData()
        assert read_cinemas_locations.read_cinemas_locations()[0] == [
            'Name', 'Address', 'LAT', 'LONG']
        assert read_cinemas_locations.read_cinemas_locations()[1][0] == "Quayside Cinema"

    def test_store_cinemas_locations(self):
        store_cinemas_loc = StoreRecreationalPlacesParkingsData()

        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        expectedresult = [[], ["Dublin Cinema", "Dublin", 0.23656, -0.1963]]

        store_cinemas_loc.read_cinemas_locations = MagicMock(
            return_value=expectedresult)
        store_cinemas_loc.store_cinemas_locations()

        fetch_cinemas_locations = Cinemas.objects(
            cinema_name="Dublin Cinema").first()

        assert fetch_cinemas_locations["cinema_name"] == "Dublin Cinema"
        assert fetch_cinemas_locations["cinema_address"] == "Dublin"
        self.assertAlmostEqual(
            fetch_cinemas_locations["cinema_lat"], Decimal(0.236), None, None, 0.005)
        self.assertAlmostEqual(
            fetch_cinemas_locations["cinema_lon"], Decimal(-0.196), None, None, 0.005)

    def test_fetch_cinemas_location(self):
        fetch_cinemas_loc = StoreRecreationalPlacesParkingsData()
        expectedresult = [[], ["Dublin Cinema", "Dublin", 0.23656, -0.1963]]

        fetch_cinemas_loc.read_cinemas_locations = MagicMock(
            return_value=expectedresult)
        fetch_cinemas_loc.store_cinemas_locations()

        cinemas_loc = fetch_cinemas_loc.fetch_cinemas_location()

        assert cinemas_loc[0]["cinema_name"] == "Dublin Cinema"
        assert cinemas_loc[0]["cinema_address"] == "Dublin"
        self.assertAlmostEqual(
            cinemas_loc[0]["cinema_lat"], 0.236, None, None, 0.005)
        self.assertAlmostEqual(
            cinemas_loc[0]["cinema_lon"], -0.196, None, None, 0.005)

    # def test_read_bus_routes(self):
    #     read_bus_routes = StoreBusRoutesData()
    #     assert read_bus_routes.read_bus_routes()[0] == [
    #         '\ufeffroute_id', 'agency_id', 'route_short_name', 'route_long_name', 'route_type']
    #     assert read_bus_routes.read_bus_routes()[1][0] == "10-100-e19-1"

    # def test_store_bus_routes(self):
    #     store_bus_stops_routes = StoreBusRoutesData()

    #     conn = get_connection()
    #     self.assertTrue(isinstance(conn, mm.MongoClient))

    #     expectedresult = [[], ["566-45-e41", 78, 'BR1', "Bus Route 1"]]

    #     store_bus_stops_routes.read_bus_routes = MagicMock(
    #         return_value=expectedresult)
    #     store_bus_stops_routes.store_bus_routes()

    #     fetch_bus_routes = BusRoutes.objects().first()

    #     assert fetch_bus_routes["route_name"] == "Bus Route 1"
    #     assert fetch_bus_routes["route_id"] == "566-45-e41"

    # def test_fetch_busroutes(self):
    #     fetch_bus_routes = StoreBusRoutesData()
    #     expectedresult = [[], ["566-45-e41", 78, 'BR1', "Bus Route 1"]]

    #     fetch_bus_routes.read_bus_routes = MagicMock(
    #         return_value=expectedresult)
    #     fetch_bus_routes.store_bus_routes()

    #     bus_routes = fetch_bus_routes.fetch_busroutes()

    #     assert bus_routes[0]["route_name"] == "Bus Route 1"
    #     assert bus_routes[0]["route_id"] == "566-45-e41"

    # def test_read_bus_trips(self):
    #     read_bus_trip = StoreBusRoutesData()
    #     assert read_bus_trip.read_bus_trips()[0] == [
    #         'route_id', 'service_id', 'trip_id', 'shape_id', 'trip_headsign', 'direction_id']
    #     assert read_bus_trip.read_bus_trips()[1][2] == "1381339.3.10-101-e19-1.261.I"

    # def test_store_bus_trips(self):
    #     store_bus_trips = StoreBusRoutesData()

    #     conn = get_connection()
    #     self.assertTrue(isinstance(conn, mm.MongoClient))

    #     expectedresult = [[], ["17-e19-34", "tyy",
    #                            "345.3.I", "1345.3.I", "Bus Station 1", "1"]]

    #     store_bus_trips.read_bus_trips = MagicMock(return_value=expectedresult)
    #     store_bus_trips.store_bus_trips()

    #     fetch_bus_trips = BusTrips.objects().first()

    #     assert fetch_bus_trips["trip_id"] == "345.3.I"
    #     assert fetch_bus_trips["route_id"] == "17-e19-34"

    # def test_store_bus_times(self):
    #     store_bus_trips = StoreBusRoutesData()

    #     conn = get_connection()
    #     self.assertTrue(isinstance(conn, mm.MongoClient))

    #     expectedresult = [[], ["17-e19-34", "tyy",
    #                            "345.3.I", "1345.3.I", "Bus Station 1", "1"]]

    #     store_bus_trips.read_bus_trips = MagicMock(return_value=expectedresult)
    #     store_bus_trips.store_bus_trips()

    #     expectedresult_timings_df = pd.DataFrame({'trip_id': ["345.3.I", "345.3.I"], 'arrival_time': ["06:20:00", "06:25:00"], 'departure_time': [
    #                                              "06:20:00", "06:25:00"], 'stop_id': ["7866R56", "7866RT7"], 'stop_sequence': [1, 2]})
    #     expectedresult_timings_df.to_csv("StoreDataTest.csv")
    #     store_bus_trips.pd.read_csv = MagicMock(
    #         return_value=pd.read_csv("StoreDataTest.csv", chunksize=2))
    #     store_bus_trips.store_bus_times()

    #     fetch_bus_trips = BusTrips.objects().first()

    #     assert fetch_bus_trips["trip_id"] == "345.3.I"
    #     assert fetch_bus_trips.stops[0]["stop_id"] == "7866R56"
    #     assert fetch_bus_trips.stops[0]["stop_arrival_time"] == "06:20:00"
    #     assert fetch_bus_trips.stops[0]["stop_departure_time"] == "06:20:00"
    #     assert fetch_bus_trips.stops[0]["stop_sequence"] == 1

    # def test_fetch_bustrips(self):
    #     fetch_bus_trips = StoreBusRoutesData()

    #     expectedresult = [[], ["17-e19-34", "tyy",
    #                            "345.3.I", "1345.3.I", "Bus Station 1", "1"]]

    #     fetch_bus_trips.read_bus_trips = MagicMock(return_value=expectedresult)
    #     fetch_bus_trips.store_bus_trips()

    #     fetch_bus_trips.pd.read_csv = MagicMock(
    #         return_value=pd.read_csv("StoreDataTest.csv", chunksize=2))
    #     fetch_bus_trips.store_bus_times()

    #     bus_trips = fetch_bus_trips.fetch_bustrips()

    #     assert bus_trips[0]["trip_id"] == "345.3.I"
    #     assert bus_trips[0]["stops"][0]["stop_id"] == "7866R56"
    #     assert bus_trips[0]["stops"][0]["stop_arrival_time"] == "06:20:00"
    #     assert bus_trips[0]["stops"][0]["stop_departure_time"] == "06:20:00"
    #     assert bus_trips[0]["stops"][0]["stop_sequence"] == 1

    # def test_read_bus_paths(self):
    #     read_bus_stops = StoreBusRoutesData()
    #     first_datapoint = read_bus_stops.read_bus_paths()['paths'][0]

    #     assert first_datapoint['start'] == '8300B1359501'
    #     assert first_datapoint['end'] == '8300B1006201'
    #     assert first_datapoint['coordinates'][0] == [53.711935, -6.352762]

    # def test_store_bus_paths(self):
    #     store_bus_stops_loc = StoreBusRoutesData()

    #     conn = get_connection()
    #     self.assertTrue(isinstance(conn, mm.MongoClient))

    #     expectedresult = {
    #         "paths": [
    #             {
    #             "start": "8300B1359501",
    #             "end": "8300B1006201",
    #             "coordinates": [
    #                 [53.711935, -6.352762]
    #             ]
    #             }
    #         ]
    #     }

    #     store_bus_stops_loc.read_bus_paths = MagicMock(
    #         return_value=expectedresult)
    #     store_bus_stops_loc.store_bus_paths()

    #     bus_path= BusPath.objects(
    #         _id='8300B13595018300B1006201').first()

    #     assert bus_path["start_stop_id"] == "8300B1359501"
    #     assert bus_path["end_stop_id"] == "8300B1006201"
    #     self.assertAlmostEqual(
    #         bus_path.coordinates[0]['lat'], Decimal(53.711935), None, None, 0.001)
    #     self.assertAlmostEqual(
    #         bus_path.coordinates[0]['lon'], Decimal(-6.352762), None, None, 0.001)

    # def test_fetch_bus_paths(self):
    #     fetch_bus_stops_loc = StoreBusRoutesData()

    #     expectedresult = {
    #         "paths": [
    #             {
    #             "start": "8300B1359501",
    #             "end": "8300B1006201",
    #             "coordinates": [
    #                 [53.711935, -6.352762]
    #             ]
    #             }
    #         ]
    #     }

    #     fetch_bus_stops_loc.read_bus_paths = MagicMock(
    #         return_value=expectedresult)
    #     fetch_bus_stops_loc.store_bus_paths()

    #     bus_paths = fetch_bus_stops_loc.fetch_bus_paths()

    #     assert bus_paths == [
    #         {
    #             '_id': '8300B13595018300B1006201',
    #             'start_stop_id': '8300B1359501',
    #             'end_stop_id': '8300B1006201',
    #             'coordinates': [
    #                 {
    #                     'lat': 53.711935,
    #                     'lon': -6.352762
    #                 }
    #             ]
    #         }
    #     ]

