from enum import Enum


class TransportType(Enum):
    TRAIN = "TRAIN"
    BUS = "BUS"
    SHIP = "SHIP"
    PLANE = "PLANE"

class SeatsClass(Enum):
    FIRST = "FIRST"
    BUSINESS = "BUSINESS"
    ECONOMY = "ECONOMY"

class BookingStatus(Enum):
    PENDING = 1
    CONFIRMED = 2
    COMPLETED = 3
    CANCELLED = 4

class SeatStatus(Enum):
    FREE = 1
    BUSY = 2
    BOOKED = 3

class Paths(Enum):
    JSON = "./Data/JSON"
    XML = "./Data/XML"
    PASSENGERS = ""
    TRIPS = "/Trips/Trips"
    TRANSPORTS = ""
    ROUTES = ""
    BOOKINGS = ""
    DOT_JSON = ".json"
    DOT_XML = ".xml"