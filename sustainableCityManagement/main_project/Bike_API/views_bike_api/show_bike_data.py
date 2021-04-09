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
from ..fetch_bikeapi import FetchBikeApi
from ..graphvalues_bike import GraphValuesBike

# API to fetch bike data -> Historical, live and locations are fetched through this API.


class ShowBikeApi(APIView):
    @classmethod
    def get(self, request, fetch_bike_api=FetchBikeApi()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "BIKE_INFO"

    # Checking the received query params and calling respective function for the response.
        try:
            inputType = request.query_params.get("type", "")

            # Fetch live data.
            if inputType == "live":
                result = fetch_bike_api.bikeapi()
                return JsonResponse(
                    {
                        "API_ID": ID,
                        "CALL_UUID": call_uuid,
                        "DATA": {
                            "RESULT": result
                        },
                        "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
                )

            # Fetch historical data.
            elif inputType == "historical":
                days_data = request.query_params.get("days_historic", "")

                result = fetch_bike_api.bikeapi(
                    historical=True, days_historical=int(days_data))
                return JsonResponse(
                    {
                        "API_ID": ID,
                        "CALL_UUID": call_uuid,
                        "DATA": {
                            "RESULT": result
                        },
                        "TIMESTAMP": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
                )

            # Fetch locations data.
            elif inputType == "locations":
                result = fetch_bike_api.bikeapi(locations=True)
                return JsonResponse(
                    {
                        "API_ID": ID,
                        "CALL_UUID": call_uuid,
                        "DATA": {
                            "RESULT": result
                        },
                        "TIME_TO_RUN": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
                )

            # If query param doesn't match any condition above.
            else:
                return JsonResponse({
                    "API_ID": ID,
                    "ERROR": "Give valid query parameters.",
                    "TIME_TO_RUN": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
                )

        except (KeyError, TypeError, ValueError):
            return JsonResponse({
                                "API_ID": ID,
                                "ERROR": "BIKE_INFO API not working, check fetch_bikeapi, and check the query parameters.",
                                "TIME_TO_RUN": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
                                )
