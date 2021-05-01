from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from .store_population import StorePopulation
import time as processTiming
import uuid

# API to fetch Ireland population used by frontend. The result consist of population estimate and year.
class IrelandPopulationView(APIView):
    @classmethod
    def get(self, request, fetch_population=StorePopulation()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "IRELAND_POPULATION_INFO"
        result = fetch_population.fetch_irish_population()
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

# API to fetch Dublin population used by frontend. The result consist of population estimate and year.
class DublinPopulationView(APIView):
    @classmethod
    def get(self, request, fetch_population=StorePopulation()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()
        ID = "DUBLIN_POPULATION_INFO"
        result = fetch_population.fetch_dublin_population()
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