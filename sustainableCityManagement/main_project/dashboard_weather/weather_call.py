import requests
import os
import sys
# from ..Config.config_handler import read_config
from datetime import date, datetime
import copy
from collections import Counter
import collections
import json

# Calling logging function for bike _API
# logger = bike_log()

# Calling Config values for processing api.
# config_vals = read_config("Weather_API")
# if config_vals is None:
#     logger.error('No data retrieved from config files.')

# Function for fetching the data from the URL (Change delay to adjust the duration to fetch data).

class FetchWeatherApi:
    def weatherapi(self):
        now_date = str(datetime.today()).split(" ")[0]
        tmp_result = []
        fetched_data = {}
        weatherCodes = {0: "Unknown",1000: "Clear",1001: "Cloudy",1100: "Mostly Clear",1101: "Partly Cloudy",
                        1102: "Mostly Cloudy",2000: "Fog",2100: "Light Fog",3000: "Light Wind",3001: "Wind",
                        3002: "Strong Wind",4000: "Drizzle",4001: "Rain",4200: "Light Rain",4201: "Heavy Rain",
                        5000: "Snow",5001: "Flurries",5100: "Light Snow",5101: "Heavy Snow",6000: "Freezing Drizzle",
                        6001: "Freezing Rain",6200: "Light Freezing Rain",6201: "Heavy Freezing Rain",7000: "Ice Pellets",
                        7101: "Heavy Ice Pellets",7102: "Light Ice Pellets",8000: "Thunderstorm"}
        
        if  os.path.exists("weather_record.json") == False or os.stat("weather_record.json").st_size == 0:
            url = "https://api.tomorrow.io/v4/timelines?location=53.42952351654325,-6.248555851275721&fields=temperature&startTime=%sT05:00:00Z&fields=humidity&fields=weatherCode&units=metric&timesteps=1d&apikey=Pmudk9ZaWPD19Kh4jjGmJeTw5ZfbCwGn"%now_date
            response = requests.request("GET", url)
            fetched_data = json.loads(response.text)
            with open('weather_record.json', 'w') as savefile:
                json.dump(fetched_data, savefile)            
        
        with open('weather_record.json','r') as json_file:
            fetched_data = json.load(json_file)
        startdate_in_data = fetched_data["data"]["timelines"][0]["startTime"]
        startdate_in_data = datetime.strptime(startdate_in_data,"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        
        result_response = {"DATE_FETCHED" : now_date}

        if startdate_in_data != now_date:
            url = "https://api.tomorrow.io/v4/timelines?location=53.42952351654325,-6.248555851275721&fields=temperature&startTime=%sT05:00:00Z&fields=humidity&fields=weatherCode&units=metric&timesteps=1d&apikey=Pmudk9ZaWPD19Kh4jjGmJeTw5ZfbCwGn"%now_date
            response = requests.request("GET", url)
            fetched_data = json.loads(response.text)
            with open('weather_record.json', 'w') as savefile:
                json.dump(fetched_data, savefile)

        item = fetched_data["data"]["timelines"][0]
        for dates_data in item["intervals"]:
            dateVal = datetime.strptime(dates_data["startTime"],"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
            result_response[dateVal] = {}
            result_response[dateVal]["TEMPERATURE"] = dates_data["values"]["temperature"]
            result_response[dateVal]["HUMIDITY"] = dates_data["values"]["humidity"]
            result_response[dateVal]["WEATHER"] = weatherCodes[dates_data["values"]["weatherCode"]]

        return result_response




a = FetchWeatherApi()
print(a.weatherapi())