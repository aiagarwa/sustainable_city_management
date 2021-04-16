import sys
from .store_bus_routes_data_in_database import StoreBusRoutesData
from datetime import datetime, timedelta
import copy
import json


class FetchBusApi:
    # Structure the bus stops data in required format to send it to frontend
    def bus_stand_locations(self, busRoutesObj=StoreBusRoutesData()):
        result_response = {}
        all_stops = busRoutesObj.fetch_busstops_location()
        counter = 0
        for location in all_stops:
            stop_custom_id = "stop_"+str(counter)
            result_response[stop_custom_id] = {}
            result_response[stop_custom_id]["STOP_ID"] = location["stop_id"]
            result_response[stop_custom_id]["STOP_NAME"] = location["stop_name"]
            result_response[stop_custom_id]["STOP_LAT"] = location["stop_lat"]
            result_response[stop_custom_id]["STOP_LON"] = location["stop_lon"]
            counter += 1
        return result_response

    # Structure the bus timings data in required format to send it to frontend
    def bus_trips_timings(self, busRoutesObj=StoreBusRoutesData()):
        result_response = {}
        counter = 0
        all_trips = busRoutesObj.fetch_bustrips()
        all_routes = busRoutesObj.fetch_busroutes()

        all_routes_dict = dict()
        for i in range(len(all_routes)):
            route_id = all_routes[i]['route_id']
            all_routes_dict[route_id] = all_routes[i]['route_name']

        for trips in all_trips:
            trip_custom_id = "trip_"+str(counter)
            result_response[trip_custom_id] = {}
            result_response[trip_custom_id]["TRIP_ID"] = trips["trip_id"]
            result_response[trip_custom_id]["ROUTE_ID"] = trips["route_id"]
            route_name = all_routes_dict[trips["route_id"]]
            result_response[trip_custom_id]["ROUTE_NAME"] = route_name
            result_response[trip_custom_id]["STOP_INFO"] = trips["stops"]
            counter += 1
        return result_response
