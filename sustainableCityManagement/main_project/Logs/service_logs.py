import sys
import logging

logger_bike = None
logger_bus = None
logger_app = None
logger_emergency = None
logger_parkings = None
logger_population = None


def bike_log():  # Creating custom logger to store logging information.
    global logger_bike
    if logger_bike is None:
        logger_bike = create_logger('bike_api')
    return logger_bike


def bus_log():  # Creating custom logger to store logging information.
    global logger_bus
    if logger_bus is None:
        logger_bus = create_logger('bus_api')
    return logger_bus


def app_log():  # Creating custom logger to store logging information.
    global logger_app
    if logger_app is None:
        logger_app = create_logger('application')
    return logger_app

def emergency_service_log():  # Creating custom logger to store logging information.
    global logger_emergency
    if logger_emergency is None:
        logger_emergency = create_logger('emergency_service_api')
    return logger_emergency

def parkings_log():  # Creating custom logger to store logging information.
    global logger_parkings
    if logger_parkings is None:
        logger_parkings = create_logger('parkings')
    return logger_parkings

def population_log():  # Creating custom logger to store logging information.
    global logger_population
    if logger_population is None:
        logger_population = create_logger('population_api')
    return logger_population

def create_logger(file_name):
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler(
        './main_project/Logs/' + file_name + '.log')
    file_handler.setLevel(logging.ERROR)

    file_handler.setFormatter(formatter)
    # To create handler that prints logging info on console.
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
