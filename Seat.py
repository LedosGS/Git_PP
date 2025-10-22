from Enums import *


class Seat:
    def __init__(self, seat_class: SeatsClass, name: str):
        self.name = name
        self.seat_class = seat_class
        self.seat_status = SeatStatus.FREE

    def __str__(self):
        return f'name: {self.name}|\t seat class: {self.seat_class.name}|\t seat_status: {self.seat_status.name}'

    def serialize(self):
        return {"name" : self.name,
                "seat_class" : self.seat_class.name,
                "seat_status" : self.seat_status.name}
