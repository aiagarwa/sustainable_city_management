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


class StoreFootfallData:
    def __init__(self):
        # self.columns = []
        self.df = None
        self.end_date = None

# Method reads the csv file containing the information of footfalls and return the list of details of footfalls
    def read_footfall(self):
        readfile = []
        not_reqd_columns = []
        self.df = pd.read_csv(
            "../sustainableCityManagement/main_project/Footfall_API/resources/pedestrian_footfall.csv")
        columns = list(self.df.columns)
        for item in columns:
            if " IN" in item or " OUT" in item:
                not_reqd_columns.append(item)
        self.df = self.df.drop(not_reqd_columns, axis=1)
        return self.df

# Method calculates the average number of footfalls 
    def calculate_average_footfall_overall(self):
        df_temp = self.read_footfall()
        mean_dict = {}
        df = df_temp.copy()
        df = df.drop(["Time"], axis=1)
        meanVals = list(df.mean(axis=0))
        columns = list(df.columns)
        for i in range(len(columns)):
            mean_dict[columns[i]] = int(meanVals[i])
        return mean_dict

# Method calculates the average number of footfalls per day 
    def calculate_average_footfall_date_based(self):
        df_temp = self.read_footfall()
        mean_dict = {}
        time_formatted = []
        df = df_temp.copy()
        for item in df["Time"]:
            time_formatted.append(datetime.strptime(
                str(item).split(" ")[0], "%d-%m-%Y"))
        df["Time"] = time_formatted
        df = df.groupby([df['Time'].dt.date]).mean().fillna(0)
        list_dates = list(dict.fromkeys(time_formatted))
        df["Time"] = list_dates
        columns = list(df.columns)[:-1]
        for location in columns:
            mean_dict[location] = {}
            for date in list_dates:
                mean_dict[location][datetime.strftime(
                    date, "%Y-%m-%d")] = int(df.loc[df.Time == str(date), location])
        return(mean_dict)

# Method stores the average number of footfalls in DB
    def store_footfall_overall(self):
        footfall_overall_data = self.calculate_average_footfall_overall()

        for item in footfall_overall_data:
            overall_data = FootfallOverall(
                location=item, count=footfall_overall_data[item])
            try:
                overall_data.save()
            except:
                pass

# Method stores the locations where footfall sensors are installed in DB
    def store_footfall_locations(self):
        footfall_overall_data = self.calculate_average_footfall_overall()
        # try:
        for item in footfall_overall_data:
            location = FootfallDateBased(location=item)
            try:
                location.save()
            except:
                pass

# Method stores the average number of footfalls per day in DB
    def store_footfall_data_datebased(self):
        fetched_footfall_data = self.calculate_average_footfall_date_based()
        for location in fetched_footfall_data:
            footfall_locations = FootfallDateBased.objects(
                location=location).first()
            if footfall_locations is not None:
                for location_details in fetched_footfall_data[location]:
                    reqd_data = FootfallInfo(
                        data_date=location_details, count=fetched_footfall_data[location][location_details])
                    footfall_locations.footfall_data.append(reqd_data)
                footfall_locations.save()  # Saves Footfall Availability Data

# Method fetches the footfall information for a single day from Database and returns it as list
    def fetch_data_from_db_for_day(self, startDate, endDate):
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

# Method fetches overall footfall information from Database and returns it as list
    def fetch_footfall_overall(self):
        q_set = FootfallOverall.objects()  # Fetch Data from DB
        json_data = q_set.to_json()
        locations = json.loads(json_data)
        return locations

# Method fetches the footfall information for the latest day from Database and returns it as list
    def get_last_date(self, reqd_location):
        pipeline = [
            {
                "$unwind": "$footfall_data"
            },
            {"$sort": {"footfall_data.data_date": -1}},
            {"$limit": 1},
            {"$project": {
                "location": "$location",
                "footfall_data": "$footfall_data",
                "_id": 0}}
        ]
        q_set = FootfallDateBased.objects(location=reqd_location).aggregate(
            *pipeline)  # Fetch Data from DB
        list_q_set = list(q_set)
        self.end_date = list_q_set[0]["footfall_data"]["data_date"].strftime(
            "%Y-%m-%d")
        return(self.end_date)

# Method fetches the footfall predictions for the next day from Database and returns it as list
    def fetch_data_from_db_with_prediction(self, days_interval, reqd_location):
        end_date = self.get_last_date(reqd_location)
        start_date = datetime.strftime(datetime.strptime(
            end_date, "%Y-%m-%d") - timedelta(days=days_interval), "%Y-%m-%d")
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
        q_set = FootfallDateBased.objects(location=reqd_location).aggregate(
            *pipeline)  # Fetch Data from DB
        list_q_set = list(q_set)
        return list_q_set, end_date
