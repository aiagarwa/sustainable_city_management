from django.urls import path
from django.conf.urls import url
from .Bike_API.views_bike_api.show_bike_data import ShowBikeApi
from .Bike_API.views_bike_api.graph_bike_data import GraphBikeData
from .Bus_API.views_bus_api.show_bus_stops import BusStopsLocations

# Building URL endpoints for API calls.
urlpatterns = [
    url(r'^bikestands_details/$', ShowBikeApi.as_view(), name ='bikestand_info'),
    url(r'^bikestands_graph/$', GraphBikeData.as_view(), name ='bikestand_info_graph'),
    url(r'^busstop_locations/$', BusStopsLocations.as_view(), name ='busstops_location_info'),
]
