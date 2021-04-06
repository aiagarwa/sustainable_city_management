from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.store_processed_bikedata_to_db import StoreProcessedBikeDataToDB
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import StoreServiceData
from main_project.Bus_API.store_bus_routes_data_in_database import StoreBusRoutesData
from main_project.Footfall_API.store_footfall_data_in_database import StoreFootfallData
from main_project.Parkings_API.store_parkingsdata_to_database import StoreParkingsData
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import StoreServiceData
from main_project.Logs.service_logs import app_log
from mongoengine import *
logger = app_log()
logger.info('Server_Starts')


def save_raw_bikedata_to_database():
    In = input("SAVE RAW DATA IN DB ? :")
    store_bikedata_to_database = StoreBikeDataToDatabase()
    if In == "yes":
        store_bikedata_to_database.save_historic_data_in_db(1)
        store_bikedata_to_database.save_bike_stands_location()
    else:
        pass


def save_processed_and_predicted_bike_data_to_database():
    In = input("SAVE PROCESSED AND PREDICTED DATA IN DB ? :")
    store_processed_bike_data_to_db = StoreProcessedBikeDataToDB()
    if In == "yes":
        store_processed_bike_data_to_db.store_bikedata(5)
        store_processed_bike_data_to_db.store_bikedata_all_locations(5)
        store_processed_bike_data_to_db.store_predict_data_in_db(5)
    else:
        pass


def save_bus_data_to_database():
    In = input("SAVE BUS DATA IN DB ? :")
    store_busdata_to_database = StoreBusRoutesData()
    if In == "yes":
        store_busdata_to_database.store_bus_stops()
        store_busdata_to_database.store_bus_routes()
        store_busdata_to_database.store_bus_trips()
        store_busdata_to_database.store_bus_times()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
        pass


def save_emergency_data_to_database():
    In = input("SAVE EMERGENCY DATA IN DB ? :")
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
    In = input("SAVE FOOTFALL DATA IN DB ? :")
    store_footfall_data_to_database = StoreFootfallData()
    if In == "yes":
        store_footfall_data_to_database.store_footfall_locations()
        store_footfall_data_to_database.store_footfall_data_datebased()
        store_footfall_data_to_database.store_footfall_overall()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
        pass


def save_parkings_data_to_database():
    In = input("SAVE PARKINGS DATA IN DB ? :")
    store_parkings_data_to_database = StoreParkingsData()
    if In == "yes":
        store_parkings_data_to_database.get_parkings_spaces_availability_live()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
        pass


def check_to_drop_database():
    In = input("DROP DATABASE? :")
    store_processed_bike_data_to_db = StoreProcessedBikeDataToDB()
    if In == "yes":
        conn = connect(
            host="mongodb://127.0.0.1:27017/sustainableCityManagementTest", alias="default")
        conn.drop_database("sustainableCityManagementTest")
    else:
        pass

def save_emergency_services_data_to_database():
    store_emergency_services = StoreServiceData()
    store_emergency_services.store_fire_stations()
    store_emergency_services.store_garda_stations()
    store_emergency_services.store_health_centers()
    store_emergency_services.store_hospitals()

def init():
    connect(
        host="mongodb://127.0.0.1:27017/sustainableCityManagementTest", alias="default")
    # check_to_drop_database()
    # save_raw_bikedata_to_database()
    # save_processed_and_predicted_bike_data_to_database()
    # save_bus_data_to_database()
    # save_footfall_data_to_database()
    # save_parkings_data_to_database()
    save_emergency_services_data_to_database()