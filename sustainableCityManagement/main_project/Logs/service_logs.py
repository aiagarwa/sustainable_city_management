import sys
import logging


def bike_log():  # Creating custom logger to store logging information.
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
    return logger
