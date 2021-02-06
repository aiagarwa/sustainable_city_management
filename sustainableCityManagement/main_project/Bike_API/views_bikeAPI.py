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
    try :
        result = fetch_bikeAPI.bikeAPI()
        ID = "bike_API"
        return JsonResponse(
            {
            "API_ID" : ID,
            "CALL_UUID" : call_uuid,
            "DATA" : {
                "RESULT" : result
            },
            "TIMESTAMP" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
            )
    except (KeyError):
        return JsonResponse(            {
            "API_ID" : ID,
            "ERROR" : "suggestBikeRelocate API not working, check fetch_bikeAPI.",
            "TIMESTAMP" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))})

