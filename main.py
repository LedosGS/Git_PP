from Transport import *
from BookingSystem import *
from Enums import *
from Trip import *

system = BookingSystem()

#
# t = Transport(TransportType.TRAIN,
#               "ivolga" ,
#               {SeatsClass.FIRST: 1,SeatsClass.BUSINESS: 2 , SeatsClass.ECONOMY: 5 },
#               {SeatsClass.FIRST: 2, SeatsClass.BUSINESS: 2, SeatsClass.ECONOMY: 5},
#               {SeatsClass.FIRST: 0, SeatsClass.BUSINESS: 0, SeatsClass.ECONOMY: 0})
#
# trip_1 = Trip("7455" , Route() , t)
# trip_2 = Trip("6844" , Route() , t)
#
# trip_1.set_seat_status(1, 1 , SeatStatus.BUSY)
# trip_2.show_sections_info()
#
# system.add_trip(trip_1)
# system.add_trip(trip_2)
# system.update_db()

system.load_db()
print(system.trips)