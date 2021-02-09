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


@api_view(['GET'])
def suggestBikeRelocate(request):
    startTime = processTiming.time()
    call_uuid = uuid.uuid4()
    ID = "bike_API"
    try :
        txt = request.query_params.get("type","")
        if txt == "live":
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
        elif txt == "historical":
            result = fetch_bikeAPI.bikeAPI(historical = True)
            return JsonResponse(
                {
                "API_ID" : ID,
                "CALL_UUID" : call_uuid,
                "DATA" : {
                    "RESULT" : result
                },
                "TIMESTAMP" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
                )

        elif txt == "locations":
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


    except (KeyError):
        return JsonResponse({
                            "API_ID" : ID,
                            "ERROR" : "suggestBikeRelocate API not working, check fetch_bikeAPI.",
                            "TIME_TO_RUN" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
                            )

