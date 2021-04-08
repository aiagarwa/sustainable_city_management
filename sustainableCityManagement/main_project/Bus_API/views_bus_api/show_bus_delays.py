import os
import uuid
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.views import APIView
import time as processTiming
from datetime import time
from rest_framework.decorators import api_view
from ..process_bus_delays import ProcessBusDelays

class BusTripDelays(APIView):
    @classmethod
    def get(self, request, bus_trip_delays = ProcessBusDelays()):
        startTime = processTiming.time()
        call_uuid = uuid.uuid4()    
        ID = "BUS_TRIP_DELAYS"
        result = bus_trip_delays.get_delay_for_trip_live()
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
