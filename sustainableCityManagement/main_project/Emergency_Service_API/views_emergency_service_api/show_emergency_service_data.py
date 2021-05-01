import os
import random
import tempfile
import uuid
import json
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
import time as processTiming
from datetime import timedelta, datetime, time, date
from rest_framework.decorators import api_view
from django.shortcuts import render
from ..fetch_emergency_service import FetchEmergencyServiceApi


# API to fetch fires stations used by frontend. The result consist of name, address, phone, email, service type, latitide and longitude.
class FireStations(APIView):
    @classmethod
    def get(self, request, fire_stations=FetchEmergencyServiceApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "FIRE_STATION_INFO"
        result = fire_stations.fire_stations_data()
        # If query param doesn't match any condition above.
        return JsonResponse(
            {
                "API_ID": ID,
                "CALL_UUID": call_uuid,
                "DATA": {
                    "RESULT": result
                },
                "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
        )

# API to fetch health centers used by frontend. The result consist of name, address, phone, latitude and longitude
class HealthCenters(APIView):
    @classmethod
    def get(self, request, health_centers=FetchEmergencyServiceApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "HEALTH_CENTER_INFO"
        result = health_centers.health_centers_data()
        # If query param doesn't match any condition above.
        return JsonResponse(
            {
                "API_ID": ID,
                "CALL_UUID": call_uuid,
                "DATA": {
                    "RESULT": result
                },
                "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
        )


# API to fetch fires stations used by frontend. The result consist of name, address, phone, division of stations, latitide and longitude.
class GardaStations(APIView):
    @classmethod
    def get(self, request, garda_stations=FetchEmergencyServiceApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "GARDA_STATION_INFO"
        result = garda_stations.garda_stations_data()
        # If query param doesn't match any condition above.
        return JsonResponse(
            {
                "API_ID": ID,
                "CALL_UUID": call_uuid,
                "DATA": {
                    "RESULT": result
                },
                "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
        )

# API to fetch health centers used by frontend. The result consist of name, address, latitude and longitude
class Hospitals(APIView):
    @classmethod
    def get(self, request, hospitals=FetchEmergencyServiceApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "HOSPITALS_INFO"
        result = hospitals.hospitals_data()
        # If query param doesn't match any condition above.
        return JsonResponse(
            {
                "API_ID": ID,
                "CALL_UUID": call_uuid,
                "DATA": {
                    "RESULT": result
                },
                "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
        )
