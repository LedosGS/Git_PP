from Transport import *
from BookingSystem import *
from Enums import *

system = BookingSystem()


t = Transport(TransportType.BUS)
t.add_section(24 , SeatsClass.ECONOMY)


t.set_seat_status(1,12, SeatStatus.BOOKED)
t.print_transport_info()

system.add_transport(t)

print(system.transports[t.transport_id])