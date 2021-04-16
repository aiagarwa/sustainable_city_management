import requests
import json
from ..Config.config_handler import read_config

class ProcessBusDelays:

    def __init__(self):
        self.config_vals = read_config("Bus_API")
    
    # Get the live data of Buses(Arrival Time, Departure Time, Delay) from API and returns.
    def get_data_from_bus_api(self):
        url = self.config_vals["api_url"]
        headers = {self.config_vals["api_key_name"]:self.config_vals["api_key_value"]}
        response = requests.get(url, headers=headers)
        bus_data = json.loads(response.text)
        bus_trip_delays = bus_data["entity"]
        return bus_trip_delays

    # Structure the live data (Delays, Arrival Time, Departure Time) in required format to send the recent stop details to frontend. 
    def get_delay_for_trip_live(self):
        bus_trip_delays=self.get_data_from_bus_api()
        result_response={}
        for trip in bus_trip_delays:
            temp = trip["trip_update"]
            if temp["trip"]["schedule_relationship"]!="CANCELED":
                delay_details = temp["stop_time_update"][-1]
                if "departure" not in delay_details:
                    temp_delay = delay_details["arrival"]
                    if "delay" not in temp_delay:
                        delay = "Not Available"
                    else:
                        delay = temp_delay["delay"]
                    result_response[trip["id"]] = {
                    "STOP_ID": delay_details["stop_id"],
                    "STOP_SEQUENCE": delay_details["stop_sequence"],
                    "DELAY": delay
                    }
                else:
                    temp_delay = delay_details["departure"]
                    if "delay" not in temp_delay:
                        delay = "Not Available"
                    else:
                        delay = temp_delay["delay"]
                    result_response[trip["id"]] = {
                        "STOP_ID": delay_details["stop_id"],
                        "STOP_SEQUENCE": delay_details["stop_sequence"],
                        "DELAY": delay
                        }
            else:
                result_response[trip["id"]] = {"STATUS":"CANCELED"}
        return result_response
