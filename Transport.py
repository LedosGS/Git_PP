from typing import List, Dict
import uuid

import Enums
from Booking import *
from Enums import *

BUS_Section = "Bus section"
TRAIN_Section = "Wagon"
PLANE_Section = "Class"
SHIP_Section = "Floor"


class Transport:
    def __init__(self, transport_type: TransportType):
        self.transport_id = uuid.uuid4()
        self.transport_type = transport_type
        # self.route = route
        self.total_seats = 0
        self.total_sections = 0
        self.sections: Dict[str, Section] = {}

    def add_section(self, seats: int, seats_class: SeatsClass):
        self.total_sections += 1
        self.total_seats += seats
        if self.transport_type == TransportType.BUS:
            section_name = BUS_Section + " " + str(len(self.sections) + 1)
            self.sections[section_name] = Section(seats, seats_class, section_name)
        elif self.transport_type == TransportType.TRAIN:
            section_name = TRAIN_Section + " " + str(len(self.sections) + 1)
            self.sections[section_name] = Section(seats, seats_class, section_name)
        elif self.transport_type == TransportType.PLANE:
            section_name = PLANE_Section + " " + str(len(self.sections) + 1)
            self.sections[section_name] = Section(seats, seats_class, section_name)
        elif self.transport_type == TransportType.SHIP:
            section_name = SHIP_Section + " " + str(len(self.sections) + 1)
            self.sections[section_name] = Section(seats, seats_class, section_name)

    def print_transport_info(self):
        for v in self.sections.values():
            print(v)

    def set_seat_status(self, number_section: int, number_seat: int, seat_status: SeatStatus):
        if self.transport_type == TransportType.BUS:
            if (self.total_sections >= number_section and len(self.sections[f'{BUS_Section} {str(number_section)}'].seats) >= number_seat):
                self.sections[f'{BUS_Section} {str(number_section)}'].seats[str(number_seat)].seat_status = seat_status
                return True
            else:   return False
        elif self.transport_type == TransportType.TRAIN:
            if (self.total_sections >= number_section and len(self.sections[f'{TRAIN_Section} {str(number_section)}'].seats) >= number_seat):
                self.sections[f'{TRAIN_Section} {str(number_section)}'].seats[str(number_seat)].seat_status = seat_status
                return True
            else:   return False
        elif self.transport_type == TransportType.PLANE:
            if (self.total_sections >= number_section and len(self.sections[f'{PLANE_Section} {str(number_section)}'].seats) >= number_seat):
                self.sections[f'{PLANE_Section} {str(number_section)}'].seats[str(number_seat)].seat_status = seat_status
                return True
            else:   return False
        elif self.transport_type == TransportType.SHIP:
            if (self.total_sections >= number_section and len(self.sections[f'{SHIP_Section} {str(number_section)}'].seats) >= number_seat):
                self.sections[f'{SHIP_Section} {str(number_section)}'].seats[str(number_seat)].seat_status = seat_status
                return True
            else:   return False


class Section:
    def __init__(self, total_seats: int, section_class: SeatsClass, name: str):
        self.name = name
        self.seats: Dict[str, Seat] = {}
        for i in range(1, total_seats + 1):
            self.seats[str(i)] = Seat(section_class, str(i))

    def __str__(self):
        seats = self.name + '\n'
        for v in self.seats.values():
            seats += v.__str__() + '\n'
        return seats


class Seat:
    def __init__(self, seat_class: SeatsClass, name: str):
        self.name = name
        self.seat_class = seat_class
        self.seat_status = SeatStatus.FREE

    def __str__(self):
        return f'name: {self.name}|\t seat class: {self.seat_class.name}|\t seat_status: {self.seat_status.name}'
