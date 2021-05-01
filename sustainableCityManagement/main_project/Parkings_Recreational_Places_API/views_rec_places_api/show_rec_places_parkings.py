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
from ..store_recreational_locations_in_db import StoreRecreationalPlacesParkingsData

# API to fetch parkings near cinemas used by frontend. The result consist of cinema name, latitude and longitude, list of 5 nearby parkings with latitude and longitudes.

class CinemasParkings(APIView):
    @classmethod
    def get(self, request, cinemas_parkings=StoreRecreationalPlacesParkingsData()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "CINEMA_PARKINGS_INFO"
        result = cinemas_parkings.fetch_cinemas_location()
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

# API to fetch parkings near beaches used by frontend. The result consist of beaches name, latitude and longitude, list of 5 nearby parkings with latitude and longitudes.
class BeachesParkings(APIView):
    @classmethod
    def get(self, request, beaches_parkings=StoreRecreationalPlacesParkingsData()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "BEACHES_PARKINGS_INFO"
        result = beaches_parkings.fetch_beaches_location()
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

# API to fetch parkings near parks used by frontend. The result consist of park name, latitude and longitude, list of 5 nearby parkings with latitude and longitudes.
class ParksParkings(APIView):
    @classmethod
    def get(self, request, parks_parkings=StoreRecreationalPlacesParkingsData()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "PARK_PARKINGS_INFO"
        result = parks_parkings.fetch_parks_location()
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

# API to fetch parkings near playing pitches used by frontend. The result consist of playing pitches name, latitude and longitude, list of 5 nearby parkings with latitude and longitudes.
class PlayingPitchesParkings(APIView):
    @classmethod
    def get(self, request, playing_pitches_parkings=StoreRecreationalPlacesParkingsData()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "PLAYING_PITCHES_PARKINGS_INFO"
        result = playing_pitches_parkings.fetch_playing_pitches_location()
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
