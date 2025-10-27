import json
import os
from typing import Dict
import json as J
import xml.etree.ElementTree as ET
import datetime
from os import mkdir,remove

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
        passengers: Dict[str, Passenger] = self.parse_passengers()
        bookings: Dict[str, Booking] = self.parse_bookings(passengers, trips)
        # routes: Dict[str, Route] = {}


        return trips , transports, passengers, bookings

    def parse_passengers(self) -> Dict[str, Passenger]:
        passengers: Dict[str, Passenger] = {}
        with open(Paths.DATA.value + Paths.PASSENGERS.value + Paths.DOT_JSON.value, 'r') as f:
            data: dict = json.load(f)
            for k, v in data.items():
                passenger = Passenger(v["document_number"],
                                      v["name"],
                                      v["birthday"],
                                      v["phone"],
                                      v["money"])
                passengers[k] = passenger
        return passengers

    def parse_bookings(self, passengers: Dict[str, Passenger], trips: Dict[str, Trip]) -> Dict[str, Booking]:
        bookings: Dict[str, Booking] = {}
        with open(Paths.DATA.value + Paths.BOOKINGS.value + Paths.DOT_JSON.value, 'r') as f:
            data: dict = json.load(f)
            for k, v in data.items():
                booking = Booking(passengers[v["passenger_document"]],
                                  trips[v['trip_number']],
                                  v["section_number"],
                                  v["seat_number"],
                                  v["cost"],
                                  v["booking_status"])
                booking.booking_id = v["id"]
                bookings[k] = booking
        return bookings
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
        self.update_bookings(bs.bookings)
        self.update_passengers(bs.passengers)


    def update_passengers(self, passengers: Dict[str, Passenger]):
        with open(Paths.DATA.value + Paths.PASSENGERS.value + Paths.DOT_JSON.value, 'w') as f:
            json_dict = {}
            for k, v in passengers.items():
                json_dict[k] = v.serialize()
            json.dump(json_dict, f, indent=4)

    def update_bookings(self, bookings: Dict[str, Booking]):
        with open(Paths.DATA.value + Paths.BOOKINGS.value + Paths.DOT_JSON.value, 'w') as f:
            json_dict = {}
            for k, v in bookings.items():
                json_dict[k] = v.serialize()
            json.dump(json_dict, f, indent=4)

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
        routes: Dict[str, Route] = {}
        return  routes

    def update(self, bs: 'BookingSystem'):
        self.save_routes(bs.routes)

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


    def save_routes(self, routes: Dict[str, Route]):
        root = ET.Element("Routes")
        for k, route in routes.items():
            root.append(self.route_to_xml(route))

        tree = ET.ElementTree(root)
        tree.write(Paths.DATA.value + Paths.ROUTES.value + Paths.DOT_XML.value, encoding="utf-8", xml_declaration=True)
        
    
    def route_to_xml(self, route: Route) -> ET.Element:
        route_root = ET.Element("route")
        ET.SubElement(route_root, "name").text = route.name
        ET.SubElement(route_root, "start_point").text = route.start_point
        ET.SubElement(route_root, "start_time").text = route.start_time
        ET.SubElement(route_root, "end_point").text = route.end_point
        ET.SubElement(route_root, "end_time").text = route.end_time
        return route_root
        

class FileSystem:
    def __init__(self):
        self.create()
        self.json = JsonSystem()
        self.xml = XmlSystem()

    def create(self):
        if (not os.path.exists(Paths.DATA.value + Paths.TRIPS.value + Paths.DOT_JSON.value)):
            trips_f = open(Paths.DATA.value + Paths.TRIPS.value + Paths.DOT_JSON.value, 'w')
            trips_f.close()
        if (not os.path.exists(Paths.DATA.value + Paths.PASSENGERS.value + Paths.DOT_JSON.value)):
            passengers_f = open(Paths.DATA.value + Paths.PASSENGERS.value + Paths.DOT_JSON.value, 'w')
            passengers_f.close()
        if (not os.path.exists(Paths.DATA.value + Paths.BOOKINGS.value + Paths.DOT_JSON.value)):
            bookings_f = open(Paths.DATA.value + Paths.BOOKINGS.value + Paths.DOT_JSON.value, 'w')
            bookings_f.close()
        if (not os.path.exists(Paths.DATA.value + Paths.TRANSPORTS.value + Paths.DOT_JSON.value)):
            transports_f = open(Paths.DATA.value + Paths.TRANSPORTS.value + Paths.DOT_JSON.value, 'w')
            transports_f.close()
        if (not os.path.exists(Paths.DATA.value + Paths.ROUTES.value + Paths.DOT_XML.value)):
            routes_f = open(Paths.DATA.value + Paths.ROUTES.value + Paths.DOT_XML.value, 'w')
            routes_f.close()

    def load(self):
        return self.json.load() , self.xml.load()

    def update(self, bs: 'BookingSystem'):
        self.json.update(bs)
        self.xml.update(bs)


    def delete(self):
        pass

    def drop_database(self):
        os.remove(Paths.DATA.value + Paths.TRIPS.value + Paths.DOT_JSON.value)
        os.remove(Paths.DATA.value + Paths.TRANSPORTS.value + Paths.DOT_JSON.value)
        os.remove(Paths.DATA.value + Paths.BOOKINGS.value + Paths.DOT_JSON.value)
        os.remove(Paths.DATA.value + Paths.PASSENGERS.value + Paths.DOT_JSON.value)
        os.remove(Paths.DATA.value + Paths.ROUTES.value + Paths.DOT_XML.value)


