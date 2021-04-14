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

# API to fetch bike data -> Historical, live and locations are fetched through this API.


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
