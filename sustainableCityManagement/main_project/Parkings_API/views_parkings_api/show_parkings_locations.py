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
from ..fetch_parkingsapi import FetchParkingsApi

# API to fetch parkings locations used by frontend. The result consist of parking name, latitude and longitude.
class ParkingsLocations(APIView):
    @classmethod
    def get(self, request, parkings = FetchParkingsApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()    
        ID = "PARKINGS_LOCATIONS"
        result = parkings.parkings_locations()
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

