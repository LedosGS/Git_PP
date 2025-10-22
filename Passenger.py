import datetime
class Passenger:
    def __init__(self,
                 document_number: str,
                 name: str,
                 birthday: datetime,
                 phone: str):
        self.document_number = document_number
        self.name = name
        self.birthday = birthday
        self.phone = phone