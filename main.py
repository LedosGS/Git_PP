import uuid
from typing import List, Dict
from enum import Enum, unique
import datetime



class Booking_System:
    def __init__(self):
        self.Routes: Dict[str, 'Route'] = {}
        self.Passengers: Dict[str, 'Passenger'] = {}
        self.Bookings: Dict[str, 'Booking'] = {}
        self.Transports: Dict[str, 'Transport'] = {}


class Route:
    def __init__(self):
        pass

class Passenger:
    def __init__(self):
        pass

class Booking:
    def __init__(self):
        pass

class Transport:
    def __init__(self):
        pass