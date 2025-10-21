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

trip = Trip("7455" , Route() , t)

trip.set_seat_status(1, 1 , SeatStatus.BUSY)
trip.show_sections_info()

system.add_trip(trip)

