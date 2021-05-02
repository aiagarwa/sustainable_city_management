from mongoengine import *

# Structure of collection storing Parks data
class Parks(Document):
    park_name = StringField(max_length=200, unique=True)
    park_address = StringField(max_length=200)
    park_area = DecimalField(precision=3)
    park_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    park_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    park_parkings = ListField(DictField())
    meta = {'collection': 'Parks_Locations'
            }

# Structure of collection storing Beaches data
class Beaches(Document):
    beach_name = StringField(max_length=200, unique=True)
    beach_id = IntField()
    beach_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    beach_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    beach_parkings = ListField(DictField())
    meta = {'collection': 'Beach_Locations'
            }

# Structure of collection storing Cinemas data
class Cinemas(Document):
    cinema_name = StringField(max_length=200, unique=True)
    cinema_address = StringField(max_length=200)
    cinema_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    cinema_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    cinema_parkings = ListField(DictField())
    meta = {'collection': 'Cinemas_Locations'
            }

# Structure of collection storing Playing Pitches data
class PlayingPitches(Document):
    facility_name = StringField(max_length=200, unique=True)
    facility_type = StringField(max_length=200)
    facility_location = StringField(max_length=200)
    facility_lat = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    facility_lon = DecimalField(precision=3, rounding='ROUND_HALF_UP')
    facility_parkings = ListField(DictField())
    meta = {'collection': 'Playing_Pithces_Locations'
            }