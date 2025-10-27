from Transport import *
from BookingSystem import *
from Enums import *
from Trip import *
from Passenger import *

import datetime

system = BookingSystem()


t = Transport(TransportType.TRAIN,
              "ivolga" ,
              {SeatsClass.FIRST: 1,SeatsClass.BUSINESS: 2 , SeatsClass.ECONOMY: 5 },
              {SeatsClass.FIRST: 2, SeatsClass.BUSINESS: 2, SeatsClass.ECONOMY: 5},
              {SeatsClass.FIRST: 10000, SeatsClass.BUSINESS: 20, SeatsClass.ECONOMY: 5})

passenger = Passenger("12345",
                      "William Smidth",
                      datetime.datetime(2000 , 3 , 9 ),
                      "89150000000",
                      10000)

route = Route("Moscow" ,
      "Samara" ,
      datetime.datetime(2025 , 3 , 9 , 22, 30),
      datetime.datetime(2025 , 3 , 10 , 12, 30))

trip_1 = Trip("7455" , route.name , t)

system.add_route(route)
system.add_transport(t)
system.add_trip(trip_1)
system.add_passenger(passenger)

t.show_info()

system.show_trips()
system.buy_seat(passenger, "7455",1,1)
system.buy_seat(passenger, "7455",2,1)

passenger.show_money()

system.trips["7455"].show_sections_info()
system.update_db(TypeBase.JSON)


# print("load---------------------------------------------------")
# system.load_db()
# print("transport\n")
# system.show_transports_info()
# print("\n\ntrips\n")
# system.show_trips_info()
# print("\n\npassengers\n")
# system.show_passengers_info()
# print("\n\nbookings\n")
# system.show_bookings_info()
# print("\n\nroutes\n")
# system.show_routes_info()

print("hello")
