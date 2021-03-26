from django.urls import path
from django.conf.urls import url
from .Bike_API.views_bike_api.show_bike_data import ShowBikeApi
from .Bike_API.views_bike_api.graph_bike_data import GraphBikeData
from .Bus_API.views_bus_api.show_bus_info import BusStopsLocations
from .Bus_API.views_bus_api.show_bus_info import BusTripsTimings
from .Bus_API.views_bus_api.show_bus_delays import BusTripDelays
from .Emergency_Service_API.views_emergency_service_api.show_emergency_service_data import FireStations
from .Emergency_Service_API.views_emergency_service_api.show_emergency_service_data import HealthCenters
from .Emergency_Service_API.views_emergency_service_api.show_emergency_service_data import GardaStations
from .Emergency_Service_API.views_emergency_service_api.show_emergency_service_data import Hospitals
from .Bus_API.views_bus_api.show_bus_stops import BusStopsLocations
from .Bus_API.views_bus_api.show_bus_paths import BusPathsAPI
# from .Parkings_API.views_parkings_api.show_parkings_availability import ParkingsAvailability
# from .Parkings_API.views_parkings_api.show_parkings_locations import ParkingsLocations
from .Parkings_API.views_parkings_api.show_parkings_availability import ParkingsAvailability
from .Parkings_API.views_parkings_api.show_parkings_locations import ParkingsLocations
from .Footfall_API.views_footfall_api.show_footfall_data import FootfallDatebasedData
from .Footfall_API.views_footfall_api.show_footfall_data import FootfallOverallData

# Building URL endpoints for API calls.
urlpatterns = [
    url(r'^bikestands_details/$', ShowBikeApi.as_view(), name='bikestand_info'),
    url(r'^bikestands_graph/$', GraphBikeData.as_view(),
        name='bikestand_info_graph'),
    url(r'^busstop_locations/$', BusStopsLocations.as_view(),
        name='busstops_location_info'),
    url(r'^busstop_timings/$', BusTripsTimings.as_view(),
        name='busstops_time_info'),
    url(r'^bustrip_delays/$', BusTripDelays.as_view(),
        name='bustrip_delay_info'),
    url(r'^bustrip_paths/$', BusPathsAPI.as_view(),
        name='bustrip_paths_info'),
    # url(r'^parkings_locations/$', ParkingsLocations.as_view(),
    #     name ='parkings_locations'),
    # url(r'^parkings_availability/$', ParkingsAvailability.as_view(), 
    #     name ='parkings_availability'),
    url(r'^footfall_overall/$', FootfallOverallData.as_view(), 
        name ='footfall_overall_data'),
    url(r'^fire_stations/$', FireStations.as_view(),
        name='fire_station_info'),
    url(r'^health_centers/$', HealthCenters.as_view(),
        name='health_centers_info'),
    url(r'^garda_stations/$', GardaStations.as_view(),
        name='garda_station_info'),
    url(r'^hospital_centers/$', Hospitals.as_view(),
        name='hospitals_centers_info'),
    url(r'^parkings_locations/$', ParkingsLocations.as_view(),
        name='parkings_locations'),
    url(r'^parkings_availability/$', ParkingsAvailability.as_view(),
        name='parkings_availability'),
    url(r'^footfall_overall/$', FootfallOverallData.as_view(),
        name='footfall_overall_data'),
    url(r'^footfall_datebased/$', FootfallDatebasedData.as_view(),
        name='footfall_datebased_data'),
]
