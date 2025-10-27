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

        self._file_system: FileSystem = FileSystem()

    def add_trip(self, trip: Trip):
        self.trips[trip.number] = trip

    def add_transport(self, transport: Transport):
        self.transports[transport.model] = transport

    def add_route(self, route: Route):
        self.routes[route.name] = route

    def add_passenger(self, passenger: Passenger):
        self.passengers[passenger.document_number] = passenger

    def add_booking(self, booking: Booking):
        self.bookings[booking.booking_id] = booking


    def buy_seat(self, passenger: Passenger, trip_number: str, section_number: int , seat_number: int ):
        trip = self.trips[trip_number]
        transport = self.transports[trip.transport_model]

        cond, section, seat, seat_class = self.trips[trip_number].set_seat_status(section_number, seat_number , SeatStatus.BUSY)
        if cond:
            cost = transport.seat_class_price[seat_class]
            booking = Booking(passenger, trip, section, seat, cost)
            self.bookings[booking.booking_id] = booking
            self.passengers[passenger.document_number].use_money(cost)
        else:
            print("error buy seat")

    def show_trips(self):
        print(self.trips.keys())

    def show_transports(self):
        print(self.transports.keys())

    def show_transports_info(self):
        for k,v in self.transports.items():
            print("\n")
            v.show_info()

    def show_trips_info(self):
        for v in self.trips.values():
            v.show_sections_info()

    def update_db(self, type_base: TypeBase):
        self._file_system.update(self)


    def load_db(self):
        self.trips, self.transports = self._file_system.load()
