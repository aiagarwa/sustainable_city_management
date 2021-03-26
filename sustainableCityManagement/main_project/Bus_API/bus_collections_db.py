from mongoengine import *

class BusStops(Document):
    stop_name = StringField(max_length=200)
    stop_id = StringField(max_length=200, unique=True)
    stop_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    stop_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    meta = {'collection': 'Bus_Stops'
            }


class BusRoutes(Document):
    route_name = StringField(max_length=200)
    route_id = StringField(max_length=200, unique=True)
    meta = {'collection': 'Bus_Routes'
            }


class StopsInfo(EmbeddedDocument):
    stop_id = StringField(max_length=200)
    stop_arrival_time = StringField()
    stop_departure_time = StringField()
    stop_sequence = IntField()


class BusTrips(Document):
    trip_id = StringField(max_length=200, unique=True)
    route_id = StringField(max_length=200)
    stops = ListField(EmbeddedDocumentField(StopsInfo))
    meta = {'collection': 'Bus_Trips'
            }


class BusTimings(Document):
    trip_id = StringField(max_length=200, unique=True)
    stop_id = StringField(max_length=200)
    stop_arrival_time = DateTimeField()
    stop_departure_time = DateTimeField()
    stop_sequence = IntField()
    meta = {'collection': 'Bus_Timings'
            }

class Coordinate(EmbeddedDocument):
    lat = DecimalField(precision=6, rounding='ROUND_HALF_UP')
    lon = DecimalField(precision=6, rounding='ROUND_HALF_UP')

class BusPath(Document):
    _id = StringField(max_length=200)
    start_stop_id = StringField(max_length=200)
    end_stop_id = StringField(max_length=200)
    coordinates = ListField(EmbeddedDocumentField(Coordinate))
    meta = {'collection': 'Bus_Paths'
            }