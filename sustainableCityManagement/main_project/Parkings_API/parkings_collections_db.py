from mongoengine import *

# Define Document Structure to store in Mongo DB. This contains Data related to Parking Spaces
class ParkingAvailability(EmbeddedDocument):
    name = StringField(max_length=200)
    area = StringField(max_length=200) # Deprecated
    availableSpaces = IntField()

class ParkingsAvailability(Document):
    updateTimestamp = DateTimeField(unique=True)
    parkings = ListField(EmbeddedDocumentField(ParkingAvailability))
    meta = {'collection': 'ParkingsAvailability'}