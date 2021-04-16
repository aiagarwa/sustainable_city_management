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
from ..store_bus_routes_data_in_database import StoreBusRoutesData

# API to fetch bus paths, used by frontend. Result will consist start and stop id of bus stops for different bus trips

class BusPathsAPI(APIView):
    @classmethod
    def get(self, request, store_bus_routes_data = StoreBusRoutesData()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()    
        ID = "BUS_PATHS_INFO"
        result = store_bus_routes_data.fetch_bus_paths()
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

