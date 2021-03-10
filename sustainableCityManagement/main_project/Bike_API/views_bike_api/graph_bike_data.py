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
from ..graphvalues_bike import GraphValuesBike

# API to fetch bike data -> Historical, live and locations are fetched through this API.

class GraphBikeData(APIView):
    # API to fetch bike graph data -> values for graph (location based or overall) are fetched through this API.
    @classmethod
    def get(self, request, graphvalues_bike = GraphValuesBike()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()    
        ID = "BIKE_INFO_GRAPH"
        result = {}
        # try :
        inputType = request.query_params.get("location_based", "")
        days_historical = request.query_params.get("days_historic", "")

        if len(days_historical) == 0 or not days_historical.isnumeric():
            raise ValueError('days_historic must contain a number')
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
