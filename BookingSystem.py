from typing import List, Dict

from FileSystem import *
from Route import *
from Passenger import *
from Booking import *
from Transport import *

class BookingSystem:
    def __init__(self):
        self.routes: Dict[str, Route] = {}
        self.passengers: Dict[str, Passenger] = {}
        self.bookings: Dict[str, Booking] = {}
        self.transports: Dict[str, Transport] = {}
        # self.file_system: FileSystem

    def add_transport(self, transport: Transport):
        transport_id = transport.transport_id.__str__()
        self.transports[transport_id] = transport




