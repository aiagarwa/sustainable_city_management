from mongoengine import *

# Structure of embedded document storing Footfalls count and date
class FootfallInfo(EmbeddedDocument):
    data_date = DateTimeField()
    count = IntField()

# Structure of collection storing Footfalls data
class FootfallDateBased(Document):
    location = StringField(max_length=200, unique=True)
    footfall_data = ListField(EmbeddedDocumentField(FootfallInfo))
    meta = {"collection": "Footfall_DateBased"}

# Structure of collection storing overall Footfalls data per location
class FootfallOverall(Document):
    location = StringField(max_length=200, unique=True)
    count = IntField()
    meta = {"collection": "Footfall_Overall"}
