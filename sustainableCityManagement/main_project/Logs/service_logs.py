import sys
import logging

logger_bike = None
logger_bus = None
logger_app = None

def bike_log():  # Creating custom logger to store logging information.
    global logger_bike
    if logger_bike is None:
        logger = create_logger('Bike_API')
        logger_bike = logger
    return logger_bike

def bus_log():  # Creating custom logger to store logging information.
    global logger_bus
    if logger_bus is None:
        logger = create_logger('Bus_API')
        logger_bus = logger
    return logger_bus

def app_log():  # Creating custom logger to store logging information.
    global logger_app
    if logger_app is None:
        logger = create_logger('Application')
        logger_app = logger
    return logger_app

def create_logger(file_name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler(
        './main_project/Logs/' + file_name +'.log')
    file_handler.setLevel(logging.ERROR)

    file_handler.setFormatter(formatter)
    # To create handler that prints logging info on console.
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger