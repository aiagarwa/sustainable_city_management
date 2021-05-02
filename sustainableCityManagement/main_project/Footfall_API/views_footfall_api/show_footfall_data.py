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
from ..fetch_footfallapi import FootfallApi

# API to fetch footfall data per day used by frontend. The result consist of location, average footfall count for a day.

class FootfallDatebasedData(APIView):
    @classmethod
    def get(self, request, footfall_datbased_data = FootfallApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()    
        ID = "FOOTFALL_DATEBASED_INFO"
        days_interval = int(request.query_params.get("days_interval", ""))
        location = request.query_params.get("location", "")
        result = footfall_datbased_data.footfall_datebased_graphvalues_predictions(location, days_interval)
        return JsonResponse(
            {
                "API_ID": ID,
                "CALL_UUID": call_uuid,
                "DATA": {
                    "RESULT": result
                },
                "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
        )


# API to fetch footfall data per day used by frontend. The result consist of location, average footfall overall for a location.
class FootfallOverallData(APIView):
    @classmethod
    def get(self, request, footfall_overall_data = FootfallApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()    
        ID = "FOOTFALL_OVERALL_INFO"
        result = footfall_overall_data.footfall_overall()
        return JsonResponse(
            {
                "API_ID": ID,
                "CALL_UUID": call_uuid,
                "DATA": {
                    "RESULT": result
                },
                "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
        )

