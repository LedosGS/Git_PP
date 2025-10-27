from typing import Dict
import uuid

from Booking import *
from Enums import *


class Transport:
    def __init__(self, transport_type: TransportType,
                 model: str,
                 cls_count_sections: Dict[SeatsClass , int],
                 cls_count_seats: Dict[SeatsClass , int],
                 seat_cls_price: Dict[SeatsClass , int]):

        self.model:str = model
        self.transport_type:TransportType = transport_type

        self.seat_class_price: Dict[SeatsClass, int] = seat_cls_price
        self.class_count_sections: Dict[SeatsClass , int] = cls_count_sections
        self.clas_count_seat: Dict[SeatsClass , int] = cls_count_seats

    def show_info(self):
        print(f'model: {self.model}\n'
              f'transport type: {self.transport_type.name}')
        for k, v in self.clas_count_seat.items():
            print(f'count seats in 1 section: {v}\t seat class: {k.name}')
        print('\n')
        for k, v in self.class_count_sections.items():
            print(f'count sections: {v}\t seat class: {k.name}')
        print('\n')
        for k, v in self.seat_class_price.items():
            print(f'seat price: {v}\t seat class: {k.name}')


    def serialize(self):
        return{"transport_type" : self.transport_type.name,
               "model" : self.model,
               "seat_class_price": serialize_dict(self.seat_class_price),
               "class_count_sections" : serialize_dict(self.class_count_sections),
               "clas_count_seat" : serialize_dict(self.clas_count_seat)}

def serialize_dict(dict: Dict[SeatsClass , int]):
    new_dict = {}
    for k, v in dict.items():
        new_dict[k.name] = v
    return new_dict