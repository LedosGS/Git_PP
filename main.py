from Transport import *
from BookingSystem import *
from Enums import *
from Trip import *

system = BookingSystem()


t = Transport(TransportType.TRAIN,
              "ivolga" ,
              {SeatsClass.FIRST: 1,SeatsClass.BUSINESS: 2 , SeatsClass.ECONOMY: 5 },
              {SeatsClass.FIRST: 2, SeatsClass.BUSINESS: 2, SeatsClass.ECONOMY: 5},
              {SeatsClass.FIRST: 0, SeatsClass.BUSINESS: 0, SeatsClass.ECONOMY: 0})

trip_1 = Trip("7455" , t)
trip_2 = Trip("6844" , t)

trip_1.set_seat_status(1, 1 , SeatStatus.BUSY)
trip_2.show_sections_info()
trip_1.show_sections_info()

system.add_trip(trip_1)
system.add_trip(trip_2)
system.update_db()

print("load---------------------------------------------------")
system.load_db()
for v in system.trips.values():
    v.show_sections_info()
