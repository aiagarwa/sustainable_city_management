from tests.Bike_API.test_store_bikedata_to_database import TestStoreBikedataToDatabase
from tests.Bike_API.test_store_processed_bikedata_to_db import TestStoreProcessedBikedataToDatabase
from tests.Bike_API.test_graphvalues_bike import TestGraphValuesBike
from tests.Bike_API.test_fetch_bikeapi import TestFetchBikeApi
from tests.Bike_API.views_bike_api.test_show_bike_data import TestShowBikeApi
from tests.Bike_API.views_bike_api.test_graph_bike_data import TestGraphBikeData
from tests.Bus_API.test_store_bus_routes_in_db import TestStoreBusRoutesData
from tests.Bus_API.test_fetch_busapi import TestFetchBusApi
from tests.Bus_API.views_bus_api.test_show_bus_data import TestBusStopsLocations
from tests.Bus_API.test_process_bus_delays import TestProcessBusDelays
from tests.Bus_API.views_bus_api.test_show_bus_delays import TestShowBusApi
from tests.Emergency_Service_API.test_store_emergency_service_data_in_database import TestStoreServiceData
from tests.Emergency_Service_API.test_fetch_emergency_service import TestFetchEmergencyServiceApi
from tests.Emergency_Service_API.views_emergency_service_api.test_show_emergency_service_data import TestEmergencyService
from tests.Footfall_API.test_store_footfall_data_in_database import TestStoreFootfalldataToDatabase
from tests.Footfall_API.test_fetch_footfallapi import TestFetchFootfallApi
from tests.Footfall_API.views_footfall_api.test_show_footfall_data import TestShowFootfallApi
from tests.Footfall_API.views_footfall_api.test_show_footfall_data import TestFootfallOverallData
from tests.ML_Models.test_bikes_uasge_prediction import TestBikeUsagePrediction
from mongoengine.connection import disconnect
import mongomock
from mongoengine import connect
disconnect(alias='default')
connect('mongoenginetest',
        host='mongomock://localhost', alias='default')
