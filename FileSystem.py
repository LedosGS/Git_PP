import json
from typing import Dict
import json as J
import xml.etree.ElementTree as ET
import datetime
import os

from Enums import *
from Trip import *
from BookingSystem import *
from Transport import *
from Section import *


class JsonSystem:
    def __init__(self):
        pass

    def load(self):
        transports: Dict[str, Transport] = self.parse_transports()
        passengers: Dict[str, Passenger] = self.parse_passengers()
        trips: Dict[str, Trip] = self.parse_trips(transports)
        bookings: Dict[str, Booking] = self.parse_bookings(passengers, trips)



        return trips , transports, passengers, bookings

    def parse_passengers(self) -> Dict[str, Passenger]:
        path = Paths.DATA.value + Paths.PASSENGERS.value + Paths.DOT_JSON.value
        if (os.path.getsize(path) == 0):
            return {}
        else:
            passengers: Dict[str, Passenger] = {}
            try:
                with open(path, 'r') as f:
                    data: dict = json.load(f)
                    for k, v in data.items():
                        passenger = Passenger(v["document_number"],
                                            v["name"],
                                            v["birthday"],
                                            v["phone"],
                                            v["money"])
                        passengers[k] = passenger
            except Exception as e:
                print(f'ошибка чтения базы пассажиров {e}')
            return passengers

    def parse_bookings(self, passengers: Dict[str, Passenger], trips: Dict[str, Trip]) -> Dict[str, Booking]:
        path = Paths.DATA.value + Paths.BOOKINGS.value + Paths.DOT_JSON.value
        if (os.path.getsize(path) == 0):
            return {}
        else:
            bookings: Dict[str, Booking] = {}
            try:
                with open(path, 'r') as f:
                    data: dict = json.load(f)
                    for k, v in data.items():
                        booking = Booking(passengers[v["passenger_document"]],
                                        trips[v['trip_number']],
                                        v["section_number"],
                                        v["seat_number"],
                                        v["cost"])
                        booking.booking_status = BookingStatus(v["booking_status"])
                        booking.booking_id = v["id"]
                        bookings[k] = booking
            except Exception as e:
                print(f'ошибка чтения базы бронирований {e}')
            return bookings
    
    def parse_trips(self, transports: Dict[str, Transport]) -> Dict[str, Trip]:
        path = Paths.DATA.value + Paths.TRIPS.value + Paths.DOT_JSON.value
        if (os.path.getsize(path) == 0):
            return {}
        else:
            trips: Dict[str, Trip] = {}
            try:
                with open(path, 'r') as f:
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
            except Exception as e:
                print(f'ошибка чтения базы поездок {e}')
            return trips

    def parse_transports(self) -> Dict[str, Transport]:
        path = Paths.DATA.value + Paths.TRANSPORTS.value + Paths.DOT_JSON.value
        if (os.path.getsize(path) == 0):
            return {}
        else:
            transports: Dict[str, Transport] = {}
            try:
                with open(path, 'r') as f:
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
            except Exception as e:
                print(f'ошибка чтения базы трспорта {e}')
            return transports

    def update(self, bs: 'BookingSystem'):
        self.update_trips(bs.trips)
        self.update_transports(bs.transports)
        self.update_bookings(bs.bookings)
        self.update_passengers(bs.passengers)

    def update_passengers(self, passengers: Dict[str, Passenger]):
        try:
            with open(Paths.DATA.value + Paths.PASSENGERS.value + Paths.DOT_JSON.value, 'w') as f:
                json_dict = {}
                for k, v in passengers.items():
                    json_dict[k] = v.serialize()
                json.dump(json_dict, f, indent=4)
        except Exception as e:
            print(f'ошибка сохранения пассажиров {e}')

    def update_bookings(self, bookings: Dict[str, Booking]):
        try:
            with open(Paths.DATA.value + Paths.BOOKINGS.value + Paths.DOT_JSON.value, 'w') as f:
                json_dict = {}
                for k, v in bookings.items():
                    json_dict[k] = v.serialize()
                json.dump(json_dict, f, indent=4)
        except Exception as e:
            print(f'ошибка сохранения поездок {e}')

    def update_trips(self, trips: Dict[str, Trip]):
        try:
            with open(Paths.DATA.value + Paths.TRIPS.value + Paths.DOT_JSON.value, 'w') as f:
                json_dict = {}
                for k, v in trips.items():
                    json_dict[k] = v.serialize()
                json.dump(json_dict, f, indent=4)
        except Exception as e:
            print(f'ошибка сохранения поездок {e}')

    def update_transports(self, transports: Dict[str, Transport]):
        try:
            with open(Paths.DATA.value + Paths.TRANSPORTS.value + Paths.DOT_JSON.value, 'w') as f:
                json_dict = {}
                for k, v in transports.items():
                    json_dict[k] = v.serialize()
                json.dump(json_dict, f, indent=4)
        except Exception as e:
            print(f'ошибка сохранения транспорта {e}')


class XmlSystem:
    def __init__(self):
        pass

    def load(self):
        path = Paths.DATA.value + Paths.ROUTES.value + Paths.DOT_XML.value
        if (os.path.getsize(path) == 0):
            return {}
        else:
            routes: Dict[str, Route] = self.load_routes()
            return  routes

    def update(self, bs: 'BookingSystem'):
        self.save_routes(bs.routes)


    def save_routes(self, routes: Dict[str, Route]):
        root = ET.Element("Routes")
        for k, route in routes.items():
            root.append(self.route_to_xml(route))

        tree = ET.ElementTree(root)
        try:
            tree.write(Paths.DATA.value + Paths.ROUTES.value + Paths.DOT_XML.value, encoding="utf-8", xml_declaration=True)
        except Exception as e:
            print(f'ошибка сохранения базы маршрутов {e}')
        
    
    def route_to_xml(self, route: Route) -> ET.Element:
        route_root = ET.Element("route")
        ET.SubElement(route_root, "name").text = route.name
        ET.SubElement(route_root, "start_point").text = route.start_point
        ET.SubElement(route_root, "start_time").text = route.start_time
        ET.SubElement(route_root, "end_point").text = route.end_point
        ET.SubElement(route_root, "end_time").text = route.end_time
        return route_root
        
    def load_routes(self):
        path = Paths.DATA.value + Paths.ROUTES.value + Paths.DOT_XML.value
        routes: Dict[str, Route] = {}
        if (os.path.getsize(path) == 0):
            return {}
        else:
            tree = ET.parse(path)
            root = tree.getroot()
            routes: Dict[str, Route] ={}
            for route_element in root.findall("route"):
                sp = route_element.find("start_point").text
                st = route_element.find("start_point").text
                ep = route_element.find("start_point").text
                et = route_element.find("start_point").text
                route = Route(sp, ep, st, et)
                routes[route.name] = route
        return routes


class FileSystem:
    def __init__(self):
        self.create()
        self.json = JsonSystem()
        self.xml = XmlSystem()

    def create(self):
        if (not os.path.exists("Data")):
            os.mkdir("Data")
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
        trips, transports, passengers, bookings = self.json.load()
        routes = self.xml.load()
        return trips, transports, passengers, bookings, routes

    def update(self, bs: 'BookingSystem'):
        self.json.update(bs)
        self.xml.update(bs)


    def drop_database(self):
        os.remove(Paths.DATA.value + Paths.TRIPS.value + Paths.DOT_JSON.value)
        os.remove(Paths.DATA.value + Paths.TRANSPORTS.value + Paths.DOT_JSON.value)
        os.remove(Paths.DATA.value + Paths.BOOKINGS.value + Paths.DOT_JSON.value)
        os.remove(Paths.DATA.value + Paths.PASSENGERS.value + Paths.DOT_JSON.value)
        os.remove(Paths.DATA.value + Paths.ROUTES.value + Paths.DOT_XML.value)


