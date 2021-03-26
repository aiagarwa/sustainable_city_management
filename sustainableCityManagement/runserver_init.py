from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.store_processed_bikedata_to_db import StoreProcessedBikeDataToDB
from main_project.Emergency_Service_API.store_emergency_service_data_in_database import StoreServiceData
from mongoengine import *
#from main_project.Logs.service_logs import app_log
# logger = app_log()
# logger.info('Server_Starts')


def save_raw_to_database():
    In = input("SAVE RAW DATA IN DB ? :")
    store_bikedata_to_database = StoreBikeDataToDatabase()
    store_emergency_service_data_to_database = StoreServiceData()
    if In == "yes":
        store_bikedata_to_database.save_historic_data_in_db(1)
        store_bikedata_to_database.save_bike_stands_location()
        # store_emergency_service_data_to_database.read_fire_stations()
        # store_emergency_service_data_to_database.store_fire_stations()
        # store_emergency_service_data_to_database.read_health_centers()
        # store_emergency_service_data_to_database.store_health_centers()
        # store_emergency_service_data_to_database.store_garda_stations()
        # store_emergency_service_data_to_database.store_garda_stations()
        # store_emergency_service_data_to_database.read_hospitals()
        # store_emergency_service_data_to_database.store_hospitals()
    else:
        pass


def save_processed_and_predicted_to_database():
    In = input("SAVE PROCESSED AND PREDICTED DATA IN DB ? :")
    store_processed_bike_data_to_db = StoreProcessedBikeDataToDB()
    if In == "yes":
        store_processed_bike_data_to_db.store_bikedata(5)
        store_processed_bike_data_to_db.store_bikedata_all_locations(5)
        store_processed_bike_data_to_db.store_predict_data_in_db(5)
    else:
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


def init():
    connect(
        host="mongodb://127.0.0.1:27017/sustainableCityManagementTest", alias="default")
    check_to_drop_database()
    save_raw_to_database()
    save_processed_and_predicted_to_database()
