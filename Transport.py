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

        self.transport_id: str = uuid.uuid4().__str__()
        self.model:str = model
        self.transport_type:TransportType = transport_type
        self.seat_class_price: Dict[SeatsClass, int] = seat_cls_price
        self.class_count_sections: Dict[SeatsClass , int] = cls_count_sections
        self.clas_count_seat: Dict[SeatsClass , int] = cls_count_seats
