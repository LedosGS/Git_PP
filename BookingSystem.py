from typing import List, Dict

from FileSystem import *
from Route import *
from Passenger import *
from Booking import *
from Transport import *
from Trip import *

class BookingSystem:
    def __init__(self):
        self.routes: Dict[str, Route] = {}
        self.passengers: Dict[str, Passenger] = {}
        self.bookings: Dict[str, Booking] = {}
        self.transports: Dict[str, Transport] = {}
        self.trips: Dict[str, Trip] = {}
        self.file_system: FileSystem = FileSystem()

    def add_trip(self, trip: Trip):
        self.trips[trip.number] = trip


    def update_db(self):
        self.file_system.update(self)


    def load_db(self):
        self.trips = self.file_system.load()
