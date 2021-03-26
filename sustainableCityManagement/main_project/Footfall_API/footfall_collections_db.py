from mongoengine import *

class FootfallInfo(EmbeddedDocument):
    data_date = DateTimeField()
    count = IntField()

class FootfallDateBased(Document):
    location = StringField(max_length=200, unique=True)
    footfall_data = ListField(EmbeddedDocumentField(FootfallInfo))
    meta = {"collection": "Footfall_DateBased"}

class FootfallOverall(Document):
    location = StringField(max_length=200, unique=True)
    count = IntField()
    meta = {"collection": "Footfall_Overall"}