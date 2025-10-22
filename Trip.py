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
    def __init__(self, number: str, transport: Transport):
        self.number: str = number
        # self.route: Route = route
        self.transport: Transport = transport
        self.sections: Dict[str, Section] = {}
        self.total_sections: int = 0
        transport_type = transport.transport_type

        section_name: str = ""
        if transport_type == TransportType.BUS:
            section_name = f'{BUS_Section} '
        elif transport_type == TransportType.TRAIN:
            section_name = f'{TRAIN_Section} '
        elif transport_type == TransportType.PLANE:
            section_name = f'{PLANE_Section} '
        elif transport_type == TransportType.SHIP:
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

    def set_seat_status(self, number_section: int, number_seat: int, seat_status: SeatStatus) -> bool:
        transport_type = self.transport.transport_type
        if transport_type == TransportType.BUS:
            if (self.total_sections >= number_section and len(self.sections[f'{BUS_Section} {str(number_section)}'].seats) >= number_seat):
                self.sections[f'{BUS_Section} {str(number_section)}'].seats[str(number_seat)].seat_status = seat_status
                return True
            else:   return False
        elif transport_type == TransportType.TRAIN:
            if (self.total_sections >= number_section and len(self.sections[f'{TRAIN_Section} {str(number_section)}'].seats) >= number_seat):
                self.sections[f'{TRAIN_Section} {str(number_section)}'].seats[str(number_seat)].seat_status = seat_status
                return True
            else:   return False
        elif transport_type == TransportType.PLANE:
            if (self.total_sections >= number_section and len(self.sections[f'{PLANE_Section} {str(number_section)}'].seats) >= number_seat):
                self.sections[f'{PLANE_Section} {str(number_section)}'].seats[str(number_seat)].seat_status = seat_status
                return True
            else:   return False
        elif transport_type == TransportType.SHIP:
            if (self.total_sections >= number_section and len(self.sections[f'{SHIP_Section} {str(number_section)}'].seats) >= number_seat):
                self.sections[f'{SHIP_Section} {str(number_section)}'].seats[str(number_seat)].seat_status = seat_status
                return True
            else:   return False

    def show_sections_info(self):
        for v in self.sections.values():
            print(v)

    def serialize(self):
        return{"number" : self.number,
               "transport" : self.transport.serialize(),
               "total_sections" : self.total_sections}
