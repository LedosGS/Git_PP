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
              {SeatsClass.FIRST: 0, SeatsClass.BUSINESS: 0, SeatsClass.ECONOMY: 0})

passenger = Passenger("12345",
                      "William Smidth",
                      datetime.datetime(2000 , 3 , 9 ),
                      "89150000000")

route = Route("Moscow" ,
      "Samara" ,
      datetime.datetime(2025 , 3 , 9 , 22, 30),
      datetime.datetime(2025 , 3 , 10 , 12, 30))

trip_1 = Trip("7455" , route , t)

system.add_route()
system.add_transport(t)
system.add_trip(trip_1)
system.add_passenger(passenger)


system.show_trips()
system.buy_seat(passenger, "7455",2,1)

system.trips["7455"].show_sections_info()
system.update_db(TypeBase.JSON)


# print("load---------------------------------------------------")
# system.load_db()
# for v in system.trips.values():
#     v.show_sections_info()
