import sys
import logging

logger = None

def bike_log():  # Creating custom logger to store logging information.
    global logger
    if logger is None:
        create_logger()
    return logger

def create_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler(
        './main_project/Logs/Bike_API.log')
    file_handler.setLevel(logging.ERROR)

    file_handler.setFormatter(formatter)
    # To create handler that prints logging info on console.
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)