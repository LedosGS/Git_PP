from typing import List, Dict
import uuid


from Enums import *
from Seat import *

class Section:
    def __init__(self, total_seats: int, section_class: SeatsClass, name: str):
        self.name = name
        self.seats: Dict[str, Seat] = {}
        self.total_seats: int = 0
        for i in range(1, total_seats + 1):
            self.total_seats += 1
            self.seats[str(i)] = Seat(section_class, str(i))


    def __str__(self):
        seats = self.name + '\n'
        for v in self.seats.values():
            seats += v.__str__() + '\n'
        return seats

    def serialize(self):
        return {"name" : self.name,
                "total_seats": self.total_seats,
                "seats" : self.serialize_seat_dict()}

    def serialize_seat_dict(self):
        new_dict = {}
        for k, v in self.seats.items():
            new_dict[k] = v.serialize()
        return new_dict
