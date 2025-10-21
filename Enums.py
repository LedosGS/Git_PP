from enum import Enum


class TransportType(Enum):
    TRAIN = 1
    BUS = 2
    SHIP = 3
    PLANE = 4

class SeatsClass(Enum):
    FIRST = 1
    BUSINESS = 2
    ECONOMY = 3

class BookingStatus(Enum):
    PENDING = 1
    CONFIRMED = 2
    COMPLETED = 3
    CANCELLED = 4

class SeatStatus(Enum):
    FREE = 1
    BUSY = 2
    BOOKED = 3

