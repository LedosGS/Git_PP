import json
from typing import Dict
import json as J
import xml as X

from Enums import *
from Trip import *
from BookingSystem import *
from Transport import *

class JsonSystem:
    def __init__(self):
        pass

    def load(self):

        with open(Paths.JSON.value + Paths.TRIPS.value + Paths.DOT_JSON.value, 'r') as f:
            trips: Dict[str, Trip] = {}
            data: dict = json.load(f)
            for k,v in data.items():
                trip = Trip(v["number"],
                            Transport(convert_transport_type(v["transport"]["transport_type"]),
                                      v["transport"]["model"],
                                      {SeatsClass.FIRST : v["transport"]["class_count_sections"]["FIRST"],
                                       SeatsClass.BUSINESS : v["transport"]["class_count_sections"]["BUSINESS"],
                                       SeatsClass.ECONOMY : v["transport"]["class_count_sections"]["ECONOMY"]},
                                      {SeatsClass.FIRST: v["transport"]["clas_count_seat"]["FIRST"],
                                       SeatsClass.BUSINESS: v["transport"]["clas_count_seat"]["BUSINESS"],
                                       SeatsClass.ECONOMY: v["transport"]["clas_count_seat"]["ECONOMY"]},
                                      {SeatsClass.FIRST: v["transport"]["seat_class_price"]["FIRST"],
                                       SeatsClass.BUSINESS: v["transport"]["seat_class_price"]["BUSINESS"],
                                       SeatsClass.ECONOMY: v["transport"]["seat_class_price"]["ECONOMY"]}
                                      ))
                trips[k] = trip
        return trips

    def update(self, bs: 'BookingSystem'):
        trips: Dict[str, 'Trip'] = bs.trips
        with open(Paths.JSON.value + Paths.TRIPS.value + Paths.DOT_JSON.value , 'w') as f:
            json_dict = {}
            for k,v in trips.items():
                json_dict[k] = v.serialize()
            json.dump(json_dict, f, indent=4)


class XmlSystem:
    def __init__(self):
        pass

class FileSystem:
    def __init__(self):
        self.json = JsonSystem()
        self.xml = XmlSystem()

    def create(self):
        pass

    def load(self):
        return self.json.load()

    def update(self, bs: 'BookingSystem'):
        self.json.update(bs)

    def delete(self):
        pass



def convert_transport_type(str: str) -> TransportType:
    if str == "TRAIN":
        return TransportType.TRAIN
    if str == "BUS":
        return TransportType.BUS
    if str == "SHIP":
        return TransportType.SHIP
    if str == "PLANE":
        return TransportType.PLANE