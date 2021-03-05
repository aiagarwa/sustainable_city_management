# # from ..Config.config_handler import read_config

# # config_vals = read_config('Bus_API')

# # def read_file():
# #     f = open(config_vals['bus_stop_file'], "r")
# #     print(f.read()) 

# # read_file()



import sys
from mongoengine import *
import requests
import json
# from datetime import datetime, timedelta
import pytz
# from ..Config.config_handler import read_config
# import logging
import csv
# # Calling logging function for Bus _API
# # logger = bike_log()
# # logger.info('Server_Starts')

# Connect to Database
# try:
# config_vals = read_config("Bus_API")
# host_db = "mongodb://127.0.0.1:%d/%s" % (
#     config_vals["db_port"], config_vals["db_name"])
# connect(config_vals["db_name"], host=host_db)
# except:
    # logger.exception('Unable to access Database')
    # raise

# # Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity



# config_vals = read_config("Bus_API")
host_db = "mongodb://127.0.0.1:27017/sustainableCityManagement"
connect("sustainableCityManagement", host=host_db)


class BusStops(Document):
    stop_name = StringField(max_length=200)
    stop_id = StringField(max_length=200, unique=True)
    stop_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    stop_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'Bus_Stops'}
#     # logger.info('BusUsage document created successfully.')


readfile = []
with open("./resources/stops.csv", "r") as f:
    readfile = list(csv.reader(f))

for i in range(1,len(readfile)):
    busstops = BusStops(stop_id = readfile[i][0],
                        stop_name = readfile[i][1].split(",")[0],
                        stop_lat = readfile[i][2],
                        stop_lon = readfile[i][3])
    try:
        busstops.save()
    except:
        pass