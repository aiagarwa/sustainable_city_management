import os
import random
import tempfile
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
def bike_details(request):
    startTime = processTiming.time()
    try :
        result = fetch_bikeAPI.bikeAPI()
        task = "bikeAPI_Location_Density"
        return JsonResponse(
            {
            "Status" : "Success",
            "Task" : task,
            "Result" : result,
            "Time_Stamp" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
            )
    except (KeyError):
        return JsonResponse({"Upload status" : "Failed"})

