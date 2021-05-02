from mongoengine import *

# Structure of embedded document storing Parkings availablilty.
class ParkingAvailability(EmbeddedDocument):
    name = StringField(max_length=200)
    area = StringField(max_length=200) # Deprecated
    availableSpaces = IntField()

# Structure of collection storing Parkings data
class ParkingsAvailability(Document):
    updateTimestamp = DateTimeField(unique=True)
    parkings = ListField(EmbeddedDocumentField(ParkingAvailability))
    meta = {'collection': 'ParkingsAvailability'}