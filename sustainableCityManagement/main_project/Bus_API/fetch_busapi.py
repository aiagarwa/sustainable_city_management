import sys
from .store_bus_routes_data_in_database import StoreBusRoutesData
from datetime import datetime, timedelta
import copy
import json


class FetchBusApi:
    def bus_stand_locations(self, busRoutesObj=StoreBusRoutesData()):
        result_response = {}
        all_stops = busRoutesObj.fetch_busstops_location()
        counter = 0
        for location in all_stops:
            stop_custom_id = "stop_"+str(counter)
            result_response[stop_custom_id] = {}
            result_response[stop_custom_id]["STOP_NAME"] = location["stop_name"]
            result_response[stop_custom_id]["STOP_LAT"] = location["stop_lat"]
            result_response[stop_custom_id]["STOP_LON"] = location["stop_lon"]
            counter += 1
        return result_response

    def bus_trips_timings(self, busRoutesObj=StoreBusRoutesData()):
        result_response = {}
        counter = 0
        all_trips = busRoutesObj.fetch_bustrips()
        for trips in all_trips:
            trip_custom_id = "trip_"+str(counter)
            result_response[trip_custom_id] = {}
            result_response[trip_custom_id]["TRIP_ID"] = trips["trip_id"]
            result_response[trip_custom_id]["ROUTE_ID"] = trips["route_id"]
            result_response[trip_custom_id]["STOP_INFO"] = trips["stops"]
            counter += 1
        return result_response

# a = FetchBusApi()
# x = a.bus_trips_timings()
# print(x)
