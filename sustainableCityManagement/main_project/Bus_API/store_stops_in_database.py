from ..Config.config_handler import read_config

config_vals = read_config('Bus_API')

def read_file():
    f = open(config_vals['bus_stop_file'], "r")
    print(f.read()) 

read_file()