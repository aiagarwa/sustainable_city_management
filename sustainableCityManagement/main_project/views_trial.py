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
# from . import wiki

@api_view(["GET"])
def helloworld(request):
    return JsonResponse(
        {
        "Result" : True,
        }
        )