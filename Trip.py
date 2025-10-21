from typing import List, Dict
import uuid

import Enums
from Booking import *
from Enums import *
from Transport import *

BUS_Section = "Bus section"
TRAIN_Section = "Wagon"
PLANE_Section = "Class"
SHIP_Section = "Floor"

class Trip:
 def __init__(self):
     self.sections: Dict[str, Section] = {}
