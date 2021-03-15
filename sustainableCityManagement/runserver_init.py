from main_project.Bike_API.store_bikedata_to_database import StoreBikeDataToDatabase
from main_project.Bike_API.store_processed_bikedata_to_db import StoreProcessedBikeDataToDB
from main_project.Logs.service_logs import bike_log
from mongoengine import *

logger = bike_log()
logger.info('Server_Starts')

def save_raw_to_database():
    In = input("SAVE RAW DATA IN DB ? :")
    store_bikedata_to_database = StoreBikeDataToDatabase()
    if In == "yes":
        store_bikedata_to_database.save_historic_data_in_db(5)
        store_bikedata_to_database.save_bike_stands_location()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
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


def init():
    connect(host="mongodb://127.0.0.1:27017/sustainableCityManagementTest", alias="default")
    save_raw_to_database()
    save_processed_and_predicted_to_database()