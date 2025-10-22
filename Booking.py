import uuid

from Enums import *
from Passenger import *
from Trip import *
class Booking:
    def __init__(self, passenger: Passenger, trip: Trip , section_number, seat_number):
        self.booking_id: str = uuid.uuid4().__str__()

        self.passenger_document: str = passenger.document_number
        self.passenger_name: str = passenger.name

        self.route_name: str = trip.route.name

        self.trip_number: str = trip.number
        self.seat_number: str = ""
        self.section_number: str = ""

        self.transport_type: TransportType = trip.transport_type
        self.transport_model: str = trip.transport_model

        self.booking_status: BookingStatus



