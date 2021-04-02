import sys
from mongoengine import *
import requests
import json
import pytz
import csv
import time as time
import pandas as pd
from datetime import datetime, timedelta
from ..Footfall_API.footfall_collections_db import FootfallInfo, FootfallDateBased, FootfallOverall
from ..Config.config_handler import read_config

config_vals = read_config("Footfall_API")

connect(host="mongodb://127.0.0.1:27017/sustainableCityManagementTest", alias="default")

class StoreFootfallData:
    def __init__(self):
        # self.columns = []
        self.df = None
        self.end_date = None
    
    def read_footfall(self):
        readfile = []
        not_reqd_columns = []
        self.df = pd.read_csv(config_vals["pedestrian_data_file"])
        # self.df = pd.read_csv("./resources/pedestrian_footfall.csv")
        columns = list(self.df.columns)
        for item in columns:
            if " IN" in item or " OUT" in item:
                not_reqd_columns.append(item)        
        self.df = self.df.drop(not_reqd_columns,axis=1)
    
    def calculate_average_footfall_overall(self):
        self.read_footfall()
        mean_dict = {}
        df = self.df.copy()
        df = df.drop(["Time"],axis=1)
        meanVals = list(df.mean(axis = 0))
        columns = list(df.columns)
        for i in range(len(columns)):
            mean_dict[columns[i]] = int(meanVals[i])
        return mean_dict

    def calculate_average_footfall_date_based(self):
        self.read_footfall()
        mean_dict = {}
        time_formatted = []
        df = self.df.copy()
        for item in df["Time"]:
            time_formatted.append(datetime.strptime(str(item).split(" ")[0], "%d-%m-%Y"))
        df["Time"] = time_formatted
        df = df.groupby([df['Time'].dt.date]).mean().fillna(0)
        list_dates = list(dict.fromkeys(time_formatted))
        df["Time"] = list_dates
        columns = list(df.columns)[:-1]
        for location in columns:
            mean_dict[location] = {}
            for date in list_dates:
                mean_dict[location][datetime.strftime(date,"%Y-%m-%d")] = int(df.loc[df.Time == str(date),location])
        return(mean_dict)

    def store_footfall_overall(self):
        footfall_overall_data = self.calculate_average_footfall_overall()

        for item in footfall_overall_data:
            overall_data = FootfallOverall(location=item,count = footfall_overall_data[item]) 
            try:
                overall_data.save()
            except:
                pass

# This method gets the data from API for a single day and store in DB.

    def store_footfall_locations(self):
        footfall_overall_data = self.calculate_average_footfall_overall()
        # try:
        for item in footfall_overall_data:
            location = FootfallDateBased(location=item)
            try:
                location.save()
            except:
                pass
        #     # logger.info(
        #     #     'Bike stand locations for Bike Usage stored into DB successfully.')
        # except:
        #     logger.exception(
        #         'Storing bike stand location for Bike Usage into DB failed!')
        #     raise


    def store_footfall_data_datebased(self):
        fetched_footfall_data = self.calculate_average_footfall_date_based()
        for location in fetched_footfall_data:
            footfall_locations = FootfallDateBased.objects(location=location).first()
            if footfall_locations is not None:
                for location_details in fetched_footfall_data[location]:
                    reqd_data = FootfallInfo(
                        data_date=location_details, count=fetched_footfall_data[location][location_details])
                    footfall_locations.footfall_data.append(reqd_data)
                footfall_locations.save()  # Saves Bike Availability Data


    def fetch_data_from_db_for_day(self, startDate, endDate):
        # start_date_str = startDate.strftime("%Y-%m-%dT00:00:00Z")
        # end_date_str = endDate.strftime("%Y-%m-%dT00:00:00Z")
        start_date = datetime.strptime(startDate, "%Y-%m-%d")
        end_date = datetime.strptime(endDate, "%Y-%m-%d")
        pipeline = [
            {"$project": {
                "location": "$location",
                "footfall_data": {"$filter": {
                    "input": "$footfall_data",
                    "as": "footfall_data",
                    "cond": {"$and": [
                        {"$lte": ["$$footfall_data.data_date", end_date]},
                        {"$gte": ["$$footfall_data.data_date", start_date]}
                    ]}
                }
                },
                "_id": 0}
             },
        ]
        q_set = FootfallDateBased.objects().aggregate(*pipeline)  # Fetch Data from DB
        list_q_set = list(q_set)
        return list_q_set


    def fetch_footfall_overall(self):
        q_set = FootfallOverall.objects()  # Fetch Data from DB
        json_data = q_set.to_json()
        locations = json.loads(json_data)
        return locations


    def fetch_data_from_db_with_prediction(self, days_interval = 20, reqd_location = "Bachelors Walk"):
        end_date = self.get_last_date()
        start_date = datetime.strftime(datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=days_interval),"%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        pipeline = [
            {"$project": {
                "location": "$location",
                "footfall_data": {"$filter": {
                    "input": "$footfall_data",
                    "as": "footfall_data",
                    "cond": {"$and": [
                        {"$lte": ["$$footfall_data.data_date", end_date]},
                        {"$gte": ["$$footfall_data.data_date", start_date]}
                        ]}
                    }
                },
                "_id": 0}
                },
            ]
        q_set = FootfallDateBased.objects(location=reqd_location).aggregate(*pipeline)  # Fetch Data from DB
        list_q_set = list(q_set)
        return list_q_set, end_date


    def get_last_date(self, reqd_location = "Bachelors Walk"):
        pipeline = [
        {
        "$unwind": "$footfall_data"
        },
        {"$sort": {"footfall_data.data_date": -1}},
        {"$limit":1},
        {"$project": { 
        "location":"$location",
        "footfall_data":"$footfall_data",
        "_id":0}}
        ]
        q_set = FootfallDateBased.objects(location=reqd_location).aggregate(*pipeline)  # Fetch Data from DB
        list_q_set = list(q_set)
        self.end_date = list_q_set[0]["footfall_data"]["data_date"].strftime("%Y-%m-%d")
        return(self.end_date)



# a = StoreFootfallData()
# print(a.fetch_data_from_db_with_prediction())
# a.store_footfall_locations()
# a.store_footfall_overall()
# a.store_footfall_data_datebased()

# print(a.fetch_data_from_db_for_day("2021-03-03","2021-03-04"))
# print(a.fetch_footfall_overall())
