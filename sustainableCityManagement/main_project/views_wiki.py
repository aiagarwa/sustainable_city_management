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
from . import wiki


@api_view(['GET'])
def wiki_trial(request):
    startTime = processTiming.time()
    try :
        txt = request.query_params.get("type","")

        task = "Wiki_Trial"
        result = wiki.WikiDetails(txt)

        return JsonResponse(
            {
            "Status" : "Success",
            "Task" : task,
            "Result" : result,
            "Time_Stamp" : "{} seconds".format(float(round(processTiming.time() - startTime,2)))}
            )
    except (KeyError):
        return JsonResponse({"Upload status" : "Failed"})

