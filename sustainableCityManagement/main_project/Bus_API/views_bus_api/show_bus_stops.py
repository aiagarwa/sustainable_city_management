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
from ..fetch_busapi import FetchBusApi

# API to fetch locations of bus stops, used by frontend. Result will consist bus stops data -Id, Latitide, longitude.

class BusStopsLocations(APIView):
    @classmethod
    def get(self, request, bus_stops_locations = FetchBusApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()    
        ID = "BUS_STOPS_INFO"
        result = bus_stops_locations.bus_stand_locations()
        return JsonResponse(
            {
                "API_ID": ID,
                "CALL_UUID": call_uuid,
                "DATA": {
                    "RESULT": result
                },
                "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
        )

