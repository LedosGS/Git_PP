import uuid

from Enums import *
from Passenger import *
from Trip import *
class Booking:
    def __init__(self, passenger: Passenger, trip: 'Trip' , section_number: str, seat_number: str, cost: int):
        self.booking_id: str = str(uuid.uuid4())

        self.passenger_document: str = passenger.document_number
        self.passenger_name: str = passenger.name

        self.route_name: str = trip.route_name

        self.trip_number: str = trip.number
        self.seat_number: str = seat_number
        self.section_number: str = section_number
        self.cost: int = cost

        self.transport_type: TransportType = trip.transport_type
        self.transport_model: str = trip.transport_model

        self.booking_status: BookingStatus = BookingStatus.PENDING

    def serialize(self):
        return {"id": self.booking_id,
                "passenger_document": self.passenger_document,
                "passenger_name": self.passenger_name,
                "route_name": self.route_name,
                "trip_number": self.trip_number,
                "section_number": self.section_number,
                "seat_number": self.seat_number,
                "cost": self.cost,
                "transport_type": self.transport_type.name,
                "transport_model": self.transport_model,
                "booking_status": self.booking_status.name
                }

    def show_booking_info(self):
        print(f'id: {self.booking_id}\n '
              f'passenger document: {self.passenger_document}\n '
              f'passenger name: {self.passenger_name}\n '
              f'route name: {self.route_name}\n '
              f'trip number: {self.trip_number}\n '
              f'section number: {self.section_number}\n '
              f'seat number: {self.seat_number}\n '
              f'cost: {self.cost}\n'
              f'transport type: {self.transport_type.name}\n'
              f'transport model: {self.transport_model}\n'
              f'booking status: {self.booking_status}\n')
