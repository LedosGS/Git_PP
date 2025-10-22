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
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class SeatStatus(Enum):
    FREE = "FREE"
    BUSY = "BUSY"
    BOOKED = "BOOKED"

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