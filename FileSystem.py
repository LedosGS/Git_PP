import json
from typing import Dict
import json as J
import xml.etree.ElementTree as ET
import datetime

from Enums import *
from Trip import *
from BookingSystem import *
from Transport import *
from Section import *


class JsonSystem:
    def __init__(self):
        pass

    def load(self) -> (Dict[str, Trip] , Dict[str, Transport]):
        transports: Dict[str, Transport] = self.parse_transports()
        trips: Dict[str, Trip] = self.parse_trips(transports)
        bookings: Dict[str, Booking] = {}
        passengers: Dict[str, Passenger] = {}
        # routes: Dict[str, Route] = {}


        return trips , transports

    def parse_trips(self, transports: Dict[str, Transport]) -> Dict[str, Trip]:
        trips: Dict[str, Trip] = {}
        with open(Paths.DATA.value + Paths.TRIPS.value + Paths.DOT_JSON.value, 'r') as f:
            data: dict = json.load(f)

            for k,v in data.items():
                trip = Trip(v["number"], v["route_number"], transports[v["transport_model"]])
                json_sections: dict = v["sections"]
                sections: Dict[str, Section] = {}
                for kj , vj in json_sections.items():
                    sections[kj] = Section(vj["total_seats"],
                                           SeatsClass(vj["seats"]["1"]["seat_class"]),
                                           vj["name"])
                    for i in range(1 ,sections[kj].total_seats+1):
                        sections[kj].seats[str(i)].seat_status = SeatStatus(json_sections[kj]["seats"][str(i)]["seat_status"])


                trip.sections = sections
                trips[k] = trip
        return trips

    def parse_transports(self) -> Dict[str, Transport]:
        transports: Dict[str, Transport] = {}

        with open(Paths.DATA.value + Paths.TRANSPORTS.value + Paths.DOT_JSON.value, 'r') as f:
            data: dict = json.load(f)
            for k, v in data.items():

                transport = Transport(TransportType(v["transport_type"]),
                                      v["model"],
                                      {SeatsClass.FIRST:v["class_count_sections"]["FIRST"],
                                       SeatsClass.BUSINESS: v["class_count_sections"]["BUSINESS"],
                                       SeatsClass.ECONOMY: v["class_count_sections"]["ECONOMY"]
                                       },
                                      {SeatsClass.FIRST:v["clas_count_seat"]["FIRST"],
                                       SeatsClass.BUSINESS: v["clas_count_seat"]["BUSINESS"],
                                       SeatsClass.ECONOMY: v["clas_count_seat"]["ECONOMY"]
                                       },
                                      {SeatsClass.FIRST:v["seat_class_price"]["FIRST"],
                                       SeatsClass.BUSINESS: v["seat_class_price"]["BUSINESS"],
                                       SeatsClass.ECONOMY: v["seat_class_price"]["ECONOMY"]
                                       },)
                transports[k] = transport
        return transports


    def update(self, bs: 'BookingSystem'):
        self.update_trips(bs.trips)
        self.update_transports(bs.transports)

    def update_trips(self, trips: Dict[str, Trip]):
        with open(Paths.DATA.value + Paths.TRIPS.value + Paths.DOT_JSON.value, 'w') as f:
            json_dict = {}
            for k, v in trips.items():
                json_dict[k] = v.serialize()
            json.dump(json_dict, f, indent=4)

    def update_transports(self, transports: Dict[str, Transport]):
        with open(Paths.DATA.value + Paths.TRANSPORTS.value + Paths.DOT_JSON.value, 'w') as f:
            json_dict = {}
            for k, v in transports.items():
                json_dict[k] = v.serialize()
            json.dump(json_dict, f, indent=4)



class XmlSystem:
    def __init__(self):
        pass

    def load(self):
        pass

    def update(self, bs: 'BookingSystem'):
        self.save_trip(bs.trips)

    def save_trip(self, trips: Dict[str, Trip]):
        root = ET.Element("Trips")
        for k, trip in trips.items():
            root.append(self.trip_to_xml(trip))

        tree = ET.ElementTree(root)
        tree.write(Paths.XML.value + Paths.TRIPS.value + Paths.DOT_XML.value, encoding="utf-8",xml_declaration=True)
    def transport_to_xml(self, transport: Transport) -> ET.Element:
        transport_root = ET.Element("transport")
        ET.SubElement(transport_root, "id").text = transport.transport_id
        ET.SubElement(transport_root, "model").text = transport.model
        ET.SubElement(transport_root, "transport_type").text = transport.transport_type.name

        seat_class_price = ET.SubElement(transport_root, "seat_class_price")
        ET.SubElement(seat_class_price, "first_seat_class_price").text = str(transport.seat_class_price[SeatsClass.FIRST])
        ET.SubElement(seat_class_price, "business_seat_class_price").text = str(transport.seat_class_price[SeatsClass.BUSINESS])
        ET.SubElement(seat_class_price, "economy_seat_class_price").text = str(transport.seat_class_price[SeatsClass.ECONOMY])

        class_count_sections = ET.SubElement(transport_root, "class_count_sections")
        ET.SubElement(class_count_sections, "first_class_count_sections").text = str(transport.class_count_sections[SeatsClass.FIRST])
        ET.SubElement(class_count_sections, "business_class_count_sections").text = str(transport.class_count_sections[SeatsClass.BUSINESS])
        ET.SubElement(class_count_sections, "economy_class_count_sections").text = str(transport.class_count_sections[SeatsClass.ECONOMY])

        clas_count_seat = ET.SubElement(transport_root, "clas_count_seat")
        ET.SubElement(clas_count_seat, "first_class_count_seat").text = str(transport.clas_count_seat[SeatsClass.FIRST])
        ET.SubElement(clas_count_seat, "business_class_count_seat").text = str(transport.clas_count_seat[SeatsClass.BUSINESS])
        ET.SubElement(clas_count_seat, "economy_class_count_seat").text = str(transport.clas_count_seat[SeatsClass.ECONOMY])

        return transport_root

    def trip_to_xml(self, trip:Trip) -> ET.Element:
        root_trip = ET.Element("trip")

        ET.SubElement(root_trip, "number").text = trip.number
        ET.SubElement(root_trip, "total_sections").text = str(trip.total_sections)
        ET.SubElement(root_trip, "transport_id").text = trip.transport_id
        root_sections = ET.SubElement(root_trip, "sections")

        for k, v in trip.sections.items():
            section_root = ET.SubElement(root_sections, "section")
            section_root.text = k
            ET.SubElement(section_root, "name").text = v.name
            ET.SubElement(section_root, "total_seats").text = str(v.total_seats)
            seats_root = ET.SubElement(section_root, "seats")
            for ks, vs in v.seats.items():
                seat_root = ET.SubElement(seats_root, "seat")
                ET.SubElement(seat_root, "name").text = vs.name
                ET.SubElement(seat_root, "seat_class").text = vs.seat_class.name
                ET.SubElement(seat_root, "seat_status").text = vs.seat_status.name


        return root_trip



class FileSystem:
    def __init__(self):
        self.json = JsonSystem()
        self.xml = XmlSystem()

    def load(self):
        return self.json.load()

    def update(self, bs: 'BookingSystem'):
        self.json.update(bs)


    def delete(self):
        pass

