from typing import List, Dict
import uuid


from Enums import *
from Seat import *

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