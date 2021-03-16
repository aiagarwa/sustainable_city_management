from mongoengine import connect
import mongomock
from tests.Bike_API.views_bike_api.test_graph_bike_data import TestGraphBikeData
from tests.Bike_API.views_bike_api.test_show_bike_data import TestShowBikeApi
from tests.Bike_API.test_fetch_bikeapi import TestFetchBikeApi
from tests.Bike_API.test_graphvalues_bike import TestGraphValuesBike
from tests.Bike_API.test_store_bikedata_to_database import TestStoreBikedataToDatabase
from tests.Bus_API.test_store_bus_routes_in_db import TestStoreBusRoutesData
from tests.Bike_API.test_graphvalues_bike import TestGraphValuesBike

connect('mongoenginetest', host='mongomock://localhost', alias='default')
