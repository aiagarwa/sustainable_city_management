from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.store_processed_bikedata_to_db import StoreProcessedBikeDataToDB
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import StoreServiceData
from main_project.Bus_API.store_bus_routes_data_in_database import StoreBusRoutesData
from main_project.Footfall_API.store_footfall_data_in_database import StoreFootfallData
from main_project.Parkings_API.store_parkingsdata_to_database import StoreParkingsData
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import StoreServiceData
from main_project.Population_API.store_population import StorePopulation
from main_project.Parkings_Recreational_Places_API.store_recreational_locations_in_db import StoreRecreationalPlacesParkingsData
from main_project.Logs.service_logs import app_log
from mongoengine import *
logger = app_log()
logger.info('Server_Starts')

import environ

# Initialise environment variables
env = environ.Env()
# environ.Env.read_env(env_file="config/dev.env")
environ.Env.read_env(env_file="config/prod.env")


def save_raw_bikedata_to_database():
    # In = input("SAVE RAW DATA IN DB ? :")
    In = "yes"
    store_bikedata_to_database = StoreBikeDataToDatabase()
    if In == "yes":
        store_bikedata_to_database.save_historic_data_in_db(1)
        store_bikedata_to_database.save_bike_stands_location()
    else:
        pass


def save_processed_and_predicted_bike_data_to_database():
    # In = input("SAVE PROCESSED AND PREDICTED DATA IN DB ? :")
    In = "yes"
    store_processed_bike_data_to_db = StoreProcessedBikeDataToDB()
    if In == "yes":
        store_processed_bike_data_to_db.store_bikedata(5)
        store_processed_bike_data_to_db.store_bikedata_all_locations(5)
        store_processed_bike_data_to_db.store_predict_data_in_db(5)
    else:
        pass


def save_bus_data_to_database():
    # In = input("SAVE BUS DATA IN DB ? :")
    In = "yes"
    store_busdata_to_database = StoreBusRoutesData()
    if In == "yes":
        store_busdata_to_database.store_bus_stops()
        store_busdata_to_database.store_bus_routes()
        store_busdata_to_database.store_bus_trips()
        store_busdata_to_database.store_bus_times()
        store_busdata_to_database.store_bus_paths()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
        pass


def save_emergency_data_to_database():
    # In = input("SAVE EMERGENCY DATA IN DB ? :")
    In = "yes"
    store_emergency_service_data_to_database = StoreServiceData()
    if In == "yes":
        store_emergency_service_data_to_database.read_fire_stations()
        store_emergency_service_data_to_database.store_fire_stations()
        store_emergency_service_data_to_database.read_health_centers()
        store_emergency_service_data_to_database.store_health_centers()
        store_emergency_service_data_to_database.store_garda_stations()
        store_emergency_service_data_to_database.store_garda_stations()
        store_emergency_service_data_to_database.read_hospitals()
        store_emergency_service_data_to_database.store_hospitals()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
        pass


def save_footfall_data_to_database():
    # In = input("SAVE FOOTFALL DATA IN DB ? :")
    In = "yes"
    store_footfall_data_to_database = StoreFootfallData()
    if In == "yes":
        store_footfall_data_to_database.store_footfall_locations()
        store_footfall_data_to_database.store_footfall_data_datebased()
        store_footfall_data_to_database.store_footfall_overall()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
        pass


def save_parkings_data_to_database():
    # In = input("SAVE PARKINGS DATA IN DB ? :")
    In = "yes"
    store_parkings_data_to_database = StoreParkingsData()
    if In == "yes":
        store_parkings_data_to_database.store_parking_spaces_availability_live()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
        pass

def save_recreational_places_parkings_data_to_database():
    # In = input("SAVE RECREATIONAL PLACES PARKINGS DATA IN DB ? :")
    In = "yes"
    store_recreational_places_parkings_data_to_database = StoreRecreationalPlacesParkingsData()
    if In == "yes":
        store_recreational_places_parkings_data_to_database.store_beaches_locations()
        store_recreational_places_parkings_data_to_database.store_cinemas_locations()
        store_recreational_places_parkings_data_to_database.store_parks_locations()
        store_recreational_places_parkings_data_to_database.store_playing_pitches_locations()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
        pass

def check_to_drop_database():
    # In = input("DROP DATABASE? :")
    In = "yes"
    store_processed_bike_data_to_db = StoreProcessedBikeDataToDB()
    if In == "yes":
        conn = connect(
            host=env('DATABASE_URI'), alias=env('DATABASE_ALIAS'))
        conn.drop_database("sustainableCityManagementTest")
    else:
        pass

def save_emergency_services_data_to_database():
    store_emergency_services = StoreServiceData()
    store_emergency_services.store_fire_stations()
    store_emergency_services.store_garda_stations()
    store_emergency_services.store_health_centers()
    store_emergency_services.store_hospitals()

def save_population_to_database():
    store_population = StorePopulation()
    store_population.store_population()

def init():
    connect(
        host=env('DATABASE_URI'), alias=env('DATABASE_ALIAS'))
    # check_to_drop_database()
    # save_raw_bikedata_to_database()
    # save_processed_and_predicted_bike_data_to_database()
    # save_bus_data_to_database()
    # save_footfall_data_to_database()
    # save_parkings_data_to_database()
    # save_emergency_services_data_to_database()
    # save_recreational_places_parkings_data_to_database()
    # save_population_to_database()