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
from ..weather_call import FetchWeatherApi

# API to fetch weather information used by frontend. The result consist of weather information of past few days and prediction for next few days

class ShowWeatherApi(APIView):
    @classmethod
    def get(self, request, fetch_weather_api = FetchWeatherApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "WEATHER_INFO"
        # try:
        result = fetch_weather_api.weatherapi()
        return JsonResponse(
            {
                "API_ID": ID,
                "CALL_UUID": call_uuid,
                "DATA": {
                    "RESULT": result
                },
                "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
        )


    # except (KeyError, TypeError, ValueError):
    #     return JsonResponse({
    #                         "API_ID": ID,
    #                         "ERROR": "WEATHER_INFO API not working, check weather_call, and check the query parameters.",
    #                         "TIME_TO_RUN": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
    #                         )