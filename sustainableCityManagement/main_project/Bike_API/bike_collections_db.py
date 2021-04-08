from mongoengine import *

# Define Embedded Document structure to store in Mongo DB. This contains Data related to Bikes availability. This is used by Bikestands Document
class BikeAvailability(EmbeddedDocument):
    bike_stands = IntField()
    available_bike_stands = IntField()
    time = DateTimeField()

# Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity
class BikeStands(Document):
    historical = ListField(EmbeddedDocumentField(BikeAvailability))
    name = StringField(max_length=200, unique=True)
    meta = {'collection': 'BikeUsage'}

# Define Document for location
class BikesStandsLocation(Document):
    name = StringField(max_length=200, required=True, unique=True)
    latitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    longitude = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'BikeStandsLocation'}

# Define Embedded Document structure to store in Mongo DB. This contains Data related to Bikes availability. This is used by Bikestands Document
class BikeAvailabilityProcessedData(EmbeddedDocument):
    total_stands = IntField()
    in_use = IntField()
    day = DateField()

# Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity


class BikeProcessedData(Document):
    data = ListField(EmbeddedDocumentField(BikeAvailabilityProcessedData))
    name = StringField(max_length=200)
    meta = {'collection': 'BikeUsageProcessed'}

# Define Embedded Document structure to store in Mongo DB. This contains Data related to Bikes availability. This is used by Bikestands Document


class BikeAvailabilityPredictedData(EmbeddedDocument):
    total_stands = IntField()
    in_use = IntField()
    day = DateField()

# Define Document Structure to store in Mongo DB. This contains Data related to Bike Stands Location and Bikes Availablity


class BikePredictedData(Document):
    data = ListField(EmbeddedDocumentField(BikeAvailabilityPredictedData))
    name = StringField(max_length=200)
    meta = {'collection': 'BikeUsagePredict'}
