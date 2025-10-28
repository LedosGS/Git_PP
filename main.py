import sys

from Transport import *
from BookingSystem import *
from Enums import *
from Trip import *
from Passenger import *
from user_interface import *

import datetime
import os

os.system('cls')
booking_system = BookingSystem()
booking_system.load_db()
booking_system.show_routes_info()
home_page()

