from mongoengine import *
from main_project.Logs.service_logs import population_log
import csv
import json

# Structure of collection storing Ireland Population data
class IrelandPopulation(Document):
    year = IntField(unique=True)
    population = IntField()
    meta = {'collection': 'Population_Ireland'}

# Structure of collection storing Dublin Population data
class DublinPopulation(Document):
    year = IntField(unique=True)
    population = IntField()
    meta = {'collection': 'Population_Dublin'}

class StorePopulation():
    def __init__(self):
        self.logger = population_log()

# Method reads the population information from csv and returns it as list
    def read_population(self):
        readfile_dublin = []
        readfile_ireland = []
        self.logger.info("Reading population files")
        with open("../sustainableCityManagement/main_project/Population_API/resources/dublin_population.csv", "r", encoding="utf8") as f:
            readfile_dublin = list(csv.reader(f))
        with open("../sustainableCityManagement/main_project/Population_API/resources/ireland_population.csv", "r", encoding="utf8") as f:
            readfile_ireland = list(csv.reader(f))
        return readfile_dublin, readfile_ireland

# Method stores the population information in Database
    def store_population(self):
        readfile_dublin, readfile_ireland = self.read_population()
        self.logger.info("Storing population Data in DB")
        for i in range(1, len(readfile_dublin)):
            dublin_population = DublinPopulation(year=readfile_dublin[i][0], population=readfile_dublin[i][1])
            try:
                dublin_population.save()
            except:
                pass
        for i in range(1, len(readfile_ireland)):
            irish_population = IrelandPopulation(year=readfile_ireland[i][0], population=readfile_ireland[i][1])
            try:
                irish_population.save()
            except:
                pass

# Method fetches and returns the Irish Population from Database
    def fetch_irish_population(self):
        q_set = IrelandPopulation.objects()  # Fetch Data from DB
        # Converts the Processed Population Data from DB into JSON format
        json_data = q_set.to_json()
        population = json.loads(json_data)
        if population is None:
            self.logger.error('Population data not retrieved from DB')
        else:
            self.logger.info("Retrieved population from DB")
        return population

# Method fetches and returns the Dublin population information from Database
    def fetch_dublin_population(self):
        q_set = DublinPopulation.objects()  # Fetch Data from DB
        # Converts the Processed Population Data from DB into JSON format
        json_data = q_set.to_json()
        population = json.loads(json_data)
        if population is None:
            self.logger.error('Population data not retrieved from DB')
        else:
            self.logger.info("Retrieved population from DB")
        return population
