from typing import Dict


from Booking import *
from Enums import *
from Transport import *
from Route import *
from Section import *

BUS_Section = "Bus section"
TRAIN_Section = "Wagon"
PLANE_Section = "Class"
SHIP_Section = "Floor"


class Trip:
    def __init__(self, number: str, route_name: str, transport: 'Transport'):
        self.number: str = number
        self.route_name: str = route_name
        self.transport_model: str = transport.model
        self.sections: Dict[str, Section] = {}
        self.total_sections: int = 0
        self.transport_type = transport.transport_type

        section_name: str = ""
        if self.transport_type == TransportType.BUS:
            section_name = f'{BUS_Section} '
        elif self.transport_type == TransportType.TRAIN:
            section_name = f'{TRAIN_Section} '
        elif self.transport_type == TransportType.PLANE:
            section_name = f'{PLANE_Section} '
        elif self.transport_type == TransportType.SHIP:
            section_name = f'{SHIP_Section} '

        section_cls = SeatsClass.FIRST
        for i in range(transport.class_count_sections[section_cls]):
            self.total_sections += 1
            sn = f'{section_name}{self.total_sections}'
            self.sections[sn] = Section(transport.clas_count_seat[section_cls], section_cls, sn)

        section_cls = SeatsClass.BUSINESS
        for i in range(transport.class_count_sections[section_cls]):
            self.total_sections += 1
            sn = f'{section_name}{self.total_sections}'
            self.sections[sn] = Section(transport.clas_count_seat[section_cls], section_cls, sn)

        section_cls = SeatsClass.ECONOMY
        for i in range(transport.class_count_sections[section_cls]):
            self.total_sections += 1
            sn = f'{section_name}{self.total_sections}'
            self.sections[sn] = Section(transport.clas_count_seat[section_cls], section_cls, sn)

    def set_seat_status(self, number_section: int, number_seat: int, seat_status: SeatStatus) -> (bool, str , str, SeatsClass):
        t_type = ""
        if self.transport_type == TransportType.BUS:
            t_type = BUS_Section
        elif self.transport_type == TransportType.TRAIN:
            t_type = TRAIN_Section
        elif self.transport_type == TransportType.PLANE:
            t_type = PLANE_Section
        elif self.transport_type == TransportType.SHIP:
            t_type = SHIP_Section

        if (self.total_sections >= number_section and len(self.sections[f'{t_type} {str(number_section)}'].seats) >= number_seat):
            s_status = self.sections[f'{t_type} {str(number_section)}'].seats[str(number_seat)].seat_status
            if (s_status == SeatStatus.BUSY or s_status == SeatStatus.BOOKED):
                return False, '' , '' , SeatStatus.BUSY
            else:
                self.sections[f'{t_type} {str(number_section)}'].seats[str(number_seat)].seat_status = seat_status
                seat_class = self.sections[f'{t_type} {str(number_section)}'].seats[str(number_seat)].seat_class
                return True, f'{t_type} {str(number_section)}', str(number_seat), seat_class
        else:
            return False, '' , '' , SeatStatus.BUSY

    def show_sections_info(self):
        for v in self.sections.values():
            print(v)

    def serialize(self):
        return{"number" : self.number,
               "transport_model" : self.transport_model,
               "total_sections" : self.total_sections,
               "route":self.route_name,
               "sections" : self.serialize_section_dict()}

    def serialize_section_dict(self):
        new_dict = {}
        for k, v in self.sections.items():
            new_dict[k] = v.serialize()
        return new_dict
