import sys

from Transport import *
from BookingSystem import *
from Enums import *
from Trip import *
from Passenger import *
from user_interface import *

import datetime
import os



os.system('cls')
booking_system = BookingSystem()
booking_system.load_db()

passenger = Passenger("12245", "Artem", datetime.date(2007, 3, 10), "8915000000", 100)


transport_1 = Transport(TransportType.TRAIN,
                        "Ivolga",
                        {SeatsClass.FIRST: 1, SeatsClass.BUSINESS: 1, SeatsClass.ECONOMY: 1},
                        {SeatsClass.FIRST: 5, SeatsClass.BUSINESS: 3, SeatsClass.ECONOMY: 10},
                        {SeatsClass.FIRST: 1000, SeatsClass.BUSINESS: 100, SeatsClass.ECONOMY: 10},)


route_1 = Route("Moscow", "Samara", datetime.datetime(2025, 10, 20), datetime.datetime(2025, 10, 21))


trip_1 = Trip("1234", route_1.name, transport_1)

booking_system.add_passenger(passenger)
booking_system.add_transport(transport_1)
booking_system.add_trip(trip_1)
booking_system.add_route(route_1)


booking_system.show_passengers_info()

# booking_system.buy_seat(passenger, trip_1.number, 1, 1)

booking_system.passengers[passenger.document_number].add_money(1000)
# #
# booking_system.show_passengers_info()

booking_system.confirm_booking(passenger.document_number, "2d9c7f59-4d85-4310-a2ea-358dc66e9abe")
booking_system.cancel_booking(passenger.document_number, "2d9c7f59-4d85-4310-a2ea-358dc66e9abe")

#
booking_system.show_bookings()
booking_system.show_passengers_info()

booking_system.show_trips_info()

booking_system.update_db()
