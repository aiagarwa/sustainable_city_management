from mongoengine import *
# Consists of the structure of all the Collections related to Buses in Mongo DB

# Structure of collection storing Bus Stops details
class BusStops(Document):
    stop_name = StringField(max_length=200)
    stop_id = StringField(max_length=200, unique=True)
    stop_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    stop_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'Bus_Stops'
            }

# Structure of collection storing Bus Routes details
class BusRoutes(Document):
    route_name = StringField(max_length=200)
    route_id = StringField(max_length=200, unique=True)
    meta = {'collection': 'Bus_Routes'
            }

# Structure of embedding document storing details of Buses at bus stops
class StopsInfo(EmbeddedDocument):
    stop_id = StringField(max_length=200)
    stop_arrival_time = StringField()
    stop_departure_time = StringField()
    stop_sequence = IntField()


# Structure of collection storing Bus Trips details
class BusTrips(Document):
    trip_id = StringField(max_length=200, unique=True)
    route_id = StringField(max_length=200)
    stops = ListField(EmbeddedDocumentField(StopsInfo))
    meta = {'collection': 'Bus_Trips'
            }

# Structure of collection storing Bus Timings
class BusTimings(Document):
    trip_id = StringField(max_length=200, unique=True)
    stop_id = StringField(max_length=200)
    stop_arrival_time = DateTimeField()
    stop_departure_time = DateTimeField()
    stop_sequence = IntField()
    meta = {'collection': 'Bus_Timings'
            }
# Structure of embedded document storing coordinates for bus routes

class Coordinate(EmbeddedDocument):
    lat = DecimalField(precision=6, rounding='ROUND_HALF_UP')
    lon = DecimalField(precision=6, rounding='ROUND_HALF_UP')

# Structure of collection storing Details of Bus Path
class BusPath(Document):
    _id = StringField(max_length=200)
    start_stop_id = StringField(max_length=200)
    end_stop_id = StringField(max_length=200)
    coordinates = ListField(EmbeddedDocumentField(Coordinate))
    meta = {'collection': 'Bus_Paths'
            }