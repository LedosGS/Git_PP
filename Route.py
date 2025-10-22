from datetime import datetime

class Route:
    def __init__(self,
                 start_point: str,
                 end_point:str ,
                 start_time:datetime,
                 end_time:datetime):

        self.name: str = start_point+ ' - ' + end_point
        self.start_point: str = start_point
        self.start_time: datetime = start_time
        self.end_point: str = end_point
        self.end_time: datetime = end_time

    def serialize(self):
        return {"name": self.name,
                "start_point": self.start_point,
                "start_time": self.start_time.__str__(),
                "end_point": self.end_point,
                "end_time": self.end_time.__str__()
                }