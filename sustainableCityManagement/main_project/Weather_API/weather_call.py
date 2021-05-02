import requests
import os
import sys
from ..Config.config_handler import read_config
from datetime import date, datetime
import copy
from collections import Counter
import collections
import json

config_vals = read_config("Weather_API")
api_url = config_vals["api_url"]
apiKey = config_vals["api_key_value"]
class FetchWeatherApi:
    def weatherapi(self):
        now_date = str(datetime.today()).split(" ")[0]
        current_time = datetime.now()
        current_time = str(current_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        url = "%s?location=53.42952351654325,-6.248555851275721&fields=temperature&startTime=%s&fields=humidity&fields=weatherCode&units=metric&timesteps=1d&apikey=%s"%(api_url,current_time,apiKey)
        tmp_result = []
        fetched_data = {}
        weatherCodes = {0: "Unknown",1000: "Clear",1001: "Cloudy",1100: "Mostly Clear",1101: "Partly Cloudy",
                        1102: "Mostly Cloudy",2000: "Fog",2100: "Light Fog",3000: "Light Wind",3001: "Wind",
                        3002: "Strong Wind",4000: "Drizzle",4001: "Rain",4200: "Light Rain",4201: "Heavy Rain",
                        5000: "Snow",5001: "Flurries",5100: "Light Snow",5101: "Heavy Snow",6000: "Freezing Drizzle",
                        6001: "Freezing Rain",6200: "Light Freezing Rain",6201: "Heavy Freezing Rain",7000: "Ice Pellets",
                        7101: "Heavy Ice Pellets",7102: "Light Ice Pellets",8000: "Thunderstorm"}
        
        if  os.path.exists("./main_project/Weather_API/weather_record.json") == False or os.stat("./main_project/Weather_API/weather_record.json").st_size == 0:
        # if  os.path.exists("weather_record.json") == False or os.stat("weather_record.json").st_size == 0:
            response = requests.request("GET", url)
            fetched_data = json.loads(response.text)
            with open('./main_project/Weather_API/weather_record.json', 'w') as savefile:
                json.dump(fetched_data, savefile, indent=4)
        
        with open('./main_project/Weather_API/weather_record.json','r') as json_file:
        # with open('weather_record.json','r') as json_file:
            fetched_data = json.load(json_file)
        try:
            if fetched_data["code"] != None:
                response = requests.request("GET", url)
                fetched_data = json.loads(response.text)
            with open('./main_project/Weather_API/weather_record.json', 'w') as savefile:
            # with open('weather_record.json', 'w') as savefile:
                    json.dump(fetched_data, savefile, indent=4)
        except:
            pass
                            
        startdate_in_data = fetched_data["data"]["timelines"][0]["startTime"]
        startdate_in_data = datetime.strptime(startdate_in_data,"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        
        result_response = {"DATE_FETCHED" : now_date}

        if startdate_in_data != now_date:
            response = requests.request("GET", url)
            fetched_data = json.loads(response.text)
            with open('./main_project/Weather_API/weather_record.json', 'w') as savefile:
            # with open('weather_record.json', 'w') as savefile:
                json.dump(fetched_data, savefile, indent=4)

        item = fetched_data["data"]["timelines"][0]
        for dates_data in item["intervals"]:
            dateVal = datetime.strptime(dates_data["startTime"],"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
            result_response[dateVal] = {}
            result_response[dateVal]["TEMPERATURE"] = dates_data["values"]["temperature"]
            result_response[dateVal]["HUMIDITY"] = dates_data["values"]["humidity"]
            result_response[dateVal]["WEATHER"] = weatherCodes[dates_data["values"]["weatherCode"]]

        return result_response
