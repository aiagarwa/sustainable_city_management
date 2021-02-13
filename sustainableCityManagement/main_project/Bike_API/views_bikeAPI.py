import os
import random
import tempfile
import uuid
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time as processTiming
from datetime import timedelta,datetime,time,date
from rest_framework.decorators import api_view
from django.shortcuts import render
from . import fetch_bikeAPI
from . import graphValues_Bike


@api_view(['GET'])
def suggestBikeRelocate(request):
    startTime = processTiming.time()
    call_uuid = uuid.uuid4()
    ID = "bike_API"
    # try :
    inputType = request.query_params.get("type","")
    if inputType == "live":
        result = fetch_bikeAPI.bikeAPI()
        return JsonResponse(
            {
            "API_ID" : ID,
            "CALL_UUID" : call_uuid,
            "DATA" : {
                "RESULT" : result
            },
            "TIMESTAMP" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
            )
    elif inputType == "historical":
        days_data = request.query_params.get("days_historic","")
        result = fetch_bikeAPI.bikeAPI(historical = True, days_historical = int(days_data))
        return JsonResponse(
            {
            "API_ID" : ID,
            "CALL_UUID" : call_uuid,
            "DATA" : {
                "RESULT" : result
            },
            "TIMESTAMP" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
            )

    elif inputType == "locations":
        result = fetch_bikeAPI.bikeAPI(locations = True)
        return JsonResponse(
            {
            "API_ID" : ID,
            "CALL_UUID" : call_uuid,
            "DATA" : {
                "RESULT" : result
            },
            "TIME_TO_RUN" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
            )

    else:
            return JsonResponse({
                    "API_ID" : ID,
                    "ERROR" : "Give valid query parameters.",
                    "TIME_TO_RUN" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
                    )


    # except (KeyError, TypeError):
    #     return JsonResponse({
    #                         "API_ID" : ID,
    #                         "ERROR" : "suggestBikeRelocate API not working, check fetch_bikeAPI, and check the query parameters.",
    #                         "TIME_TO_RUN" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
    #                         )


@api_view(['GET'])
def suggestBikeRelocate_graph(request):
    startTime = processTiming.time()
    call_uuid = uuid.uuid4()
    ID = "bike_API_Graph"
    result = {}
    # try :
    inputType = request.query_params.get("location_based","")
    days_data = int(request.query_params.get("days_historic",""))
    if inputType == "yes":
        result = graphValues_Bike.graphValue_Call(days_historical = days_data)
    elif inputType == "no":
        result = graphValues_Bike.graphValue_Call(locationsBased = False, days_historical = days_data)
    else:
        return JsonResponse({
                "API_ID" : ID,
                "ERROR" : "Give valid query parameters.",
                "TIME_TO_RUN" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
                )
    return JsonResponse(
        {
        "API_ID" : ID,
        "CALL_UUID" : call_uuid,
        "DATA" : {
            "RESULT" : result
        },
        "TIMESTAMP" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
        )

    # except (KeyError, TypeError):
    #     return JsonResponse({
    #                         "API_ID" : ID,
    #                         "ERROR" : "suggestBikeRelocate API not working, check fetch_bikeAPI, and check the query parameters.",
    #                         "TIME_TO_RUN" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
    #                         )

