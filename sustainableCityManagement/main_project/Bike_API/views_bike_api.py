import os
import random
import tempfile
import uuid
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import time as processTiming
from datetime import timedelta, datetime, time, date
from rest_framework.decorators import api_view
from django.shortcuts import render
from . import fetch_bikeapi
from . import graphvalues_bike

# API to fetch bike data -> Historical, live and locations are fetched through this API.


@api_view(['GET'])
def show_bike_data(request):
    startTime = processTiming.time()
    call_uuid = uuid.uuid4()
    ID = "BIKE_INFO"

# Checking the received query params and calling respective function for the response.
    try:
        inputType = request.query_params.get("type", "")

        # Fetch live data.
        if inputType == "live":
            result = fetch_bikeapi.bikeapi()
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
            result = fetch_bikeapi.bikeapi(
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
            result = fetch_bikeapi.bikeapi(locations=True)
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

    except (KeyError, TypeError):
        return JsonResponse({
                            "API_ID": ID,
                            "ERROR": "BIKE_INFO API not working, check fetch_bikeapi, and check the query parameters.",
                            "TIME_TO_RUN": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
                            )

# API to fetch bike graph data -> values for graph (location based or overall) are fetched through this API.


@api_view(['GET'])
def graph_bike_data(request):
    startTime = processTiming.time()
    call_uuid = uuid.uuid4()
    ID = "BIKE_INFO_GRAPH"
    result = {}
    # try :
    inputType = request.query_params.get("location_based", "")
    days_historical = request.query_params.get("days_historic", "")
    if len(days_historical) != 0:
        days_data = int(days_historical)

    # If location_based is yes, then graph values for all the locations is delivered.
    if inputType == "yes":
        result = graphvalues_bike.graphvalue_call_locationbased(
            days_historical=days_data)

    # If location_based is no, then graph values are delivered in cumulative format from all the locations.
    elif inputType == "no":
        result = graphvalues_bike.graphvalue_call_overall(
            days_historical=days_data)

    else:
        return JsonResponse({
            "API_ID": ID,
            "ERROR": "Give valid query parameters.",
            "TIME_TO_RUN": "{} seconds".format(float(round(processTiming.time() - startTime, 2)))}
        )

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

    # except (KeyError, TypeError):
    #     return JsonResponse({
    #                         "API_ID" : ID,
    #                         "ERROR" : "BIKE_INFO_GRAPH API not working, check fetch_bikeAPI, and check the query parameters.",
    #                         "TIME_TO_RUN" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
    #                         )
