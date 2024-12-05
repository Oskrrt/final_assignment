import sys

import logger
from config_manager import ConfigManager
from logger import *
from functools import wraps

from tarjan_planner.calculations import calculate_price
from user_interface_modules.user_interface import init_ui

RELATIVES = ConfigManager.load_config("relatives")
TRANSPORT_METHODS = ConfigManager.load_config("modes_of_transport")

@time_this
def init_route_planner():
    #init_ui()
    try:
        find_most_efficient_route()
    except Exception as e:
        log_error(e)

def find_most_efficient_route():
    relative_coordinates = get_coordinates()
    calculate_price(TRANSPORT_METHODS, relative_coordinates)

def get_coordinates():
    longitudes = []
    latitudes = []
    for relative in RELATIVES:
        latitude = RELATIVES[relative]["latitude"]
        longitude = RELATIVES[relative]["longitude"]
        longitudes.append(longitude)
        latitudes.append(latitude)

    return longitudes, latitudes
# def test_error():
#     try:
#         raise Exception("test exception")
#     except Exception as e:
#         log_error(e)