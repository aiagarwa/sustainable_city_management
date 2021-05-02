import pandas as pd
from datetime import datetime, timedelta, date
from django.test import TestCase
from unittest.mock import MagicMock
from main_project.Population_API.store_population import StorePopulation, IrelandPopulation, DublinPopulation
from mongoengine import *
import mongomock as mm
from decimal import Decimal
import json


class TestStorePopulation(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    # Testing hospital functions over database.
    def test_read_hospitals(self):
        read_population = StorePopulation()
        readfile_dublin, readfile_ireland = read_population.read_population()

        assert readfile_dublin[0] == ['year', 'population']
        assert readfile_dublin[1][0] == "1960"

        assert readfile_ireland[0] == ['year', 'population']
        assert readfile_ireland[1][0] == "1960"

    def test_store_hospitals(self):
        store_service = StorePopulation()
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        store_service.store_population()

        fetch_irish_population_1960 = IrelandPopulation.objects(year=1960).first()
        fetch_dublin_population_1960 = DublinPopulation.objects(year=1960).first()

        assert fetch_irish_population_1960["year"] == 1960
        assert fetch_irish_population_1960["population"] == 2832000
        assert fetch_dublin_population_1960["year"] == 1960
        assert fetch_dublin_population_1960["population"] == 661000

    def test_fetch_ireland_population(self):
        fetch_service = StorePopulation()
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        fetch_service.store_population()

        irish_population = fetch_service.fetch_irish_population()

        assert irish_population[0]["year"] == 1960
        assert irish_population[0]["population"] == 2832000

    def test_fetch_dublin_population(self):
        fetch_service = StorePopulation()
        conn = get_connection()
        self.assertTrue(isinstance(conn, mm.MongoClient))

        fetch_service.store_population()

        dublin_population = fetch_service.fetch_dublin_population()

        assert dublin_population[0]["year"] == 1960
        print(dublin_population[0]["population"])
        assert dublin_population[0]["population"] == 661000
