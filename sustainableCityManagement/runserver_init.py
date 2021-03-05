from main_project.Bike_API.store_bikedata_to_database import save_historic_data_in_db
from main_project.Bike_API.store_bikedata_to_database import save_bike_stands_location
from main_project.Bike_API.store_processed_bikedata_to_db import store_bikedata
from main_project.Bike_API.store_processed_bikedata_to_db import store_bikedata_all_locations
from main_project.Bike_API.store_processed_bikedata_to_db import store_predict_data_in_db
from main_project.Logs.service_logs import bike_log

logger = bike_log()
logger.info('Server_Starts')

def save_raw_to_database():
    In = input("SAVE RAW DATA IN DB ? :")
    if In == "yes":
        save_historic_data_in_db(5)
        save_bike_stands_location()
    else:
        logger.error('Storing raw data in DB failed because of key(yes) error')
        pass

def save_processed_and_predicted_to_database():
    In = input("SAVE PROCESSED AND PREDICTED DATA IN DB ? :")
    if In == "yes":
        store_bikedata(5)
        store_bikedata_all_locations(5)
        store_predict_data_in_db(5)
    else:
        pass


def init():
    save_raw_to_database()
    save_processed_and_predicted_to_database()