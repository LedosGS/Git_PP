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

        self._file_system: 'FileSystem' = FileSystem()

    def add_trip(self, trip: Trip):
        self.trips[trip.number] = trip

    def add_transport(self, transport: Transport):
        self.transports[transport.model] = transport

    def add_route(self, route: Route):
        self.routes[route.name] = route

    def add_passenger(self, passenger: Passenger):
        self.passengers[passenger.document_number] = passenger

    def buy_seat(self, passenger: Passenger, trip_number: str, section_number: int, seat_number: int):
        trip = self.trips[trip_number]
        transport = self.transports[trip.transport_model]

        cond, section, seat, seat_class = self.trips[trip_number].set_seat_status(section_number, seat_number,
                                                                                  SeatStatus.BUSY)
        if cond:
            cost = transport.seat_class_price[seat_class]
            booking = Booking(passenger, trip, section, seat, cost)
            self.bookings[booking.booking_id] = booking
            if (self.passengers[passenger.document_number].get_money() >= cost):
                self.passengers[passenger.document_number].use_money(cost)
                booking.booking_status = BookingStatus.CONFIRMED
                self.bookings[booking.booking_id] = booking
            else:
                self.trips[trip_number].seat_status(section_number, seat_number, SeatStatus.FREE)
                print("не хватает денег, пополните счёт и попробуйте позднее")
                print("номер бронирования:", booking.booking_id)
        else:
            print("ошибка, место занято")

    def book_seat(self, passenger: Passenger, trip_number: str, section_number: int, seat_number: int):
        trip = self.trips[trip_number]
        transport = self.transports[trip.transport_model]

        cond, section, seat, seat_class = self.trips[trip_number].set_seat_status(section_number, seat_number,
                                                                                  SeatStatus.BOOKED)
        if cond:
            cost = transport.seat_class_price[seat_class]
            booking = Booking(passenger, trip, section, seat, cost)
            self.bookings[booking.booking_id] = booking
        else:
            print("ошибка, место занято")

    def cancel_booking(self, passenger_document: str, booking_id: str):
        booking = self.bookings[booking_id]
        self.trips[booking.trip_number].seat_status(int(booking.section_number), int(booking.seat_number), SeatStatus.FREE)
        self.bookings[booking_id].booking_status = BookingStatus.CANCELLED
        self.passengers[passenger_document].add_money(booking.cost // 2)

    def confirm_booking(self, passenger_document: str, booking_id: str):
        booking = self.bookings[booking_id]
        self.trips[booking.trip_number].set_seat_status(int(booking.section_number), int(booking.seat_number), SeatStatus.BUSY)
        if (self.passengers[passenger_document].get_money() >= booking.cost):
            self.passengers[passenger_document].use_money(booking.cost)
            booking.booking_status = BookingStatus.CONFIRMED
            self.bookings[booking.booking_id] = booking
        else:
            self.trips[booking.trip_number].set_seat_status(int(booking.section_number), int(booking.seat_number),
                                                            SeatStatus.BOOKED)
            print("не хватает денег, пополните счёт и попробуйте позднее")
            print("номер бронирования:", booking.booking_id)

    def show_trips(self):
        print(self.trips.keys())

    def show_transports(self):
        for k in self.transports.keys():
            print(k)

    def show_bookings(self):
        for k in self.bookings.keys():
            print(k)

    def show_routes(self):
        for k in self.routes.keys():
            print(k)

    def show_passengers(self):
        for k in self.passengers.keys():
            print(k)

    def show_transports_info(self):
        for k, v in self.transports.items():
            v.show_info()
            print('\n')

    def show_trips_info(self):
        for v in self.trips.values():
            v.show_sections_info()
            print('\n')

    def show_passengers_info(self):
        for v in self.passengers.values():
            v.show_passenger_info()
            print('\n')

    def show_bookings_info(self):
        for v in self.bookings.values():
            v.show_booking_info()
            print('\n')

    def show_routes_info(self):
        for v in self.routes.values():
            v.show_route_info()
            print('\n')

    def update_db(self):
        self._file_system.update(self)

    def load_db(self):
        self.trips, self.transports, self.passengers, self.bookings, self.routes = self._file_system.load()

    def drop_db(self):
        self._file_system.drop_database()
