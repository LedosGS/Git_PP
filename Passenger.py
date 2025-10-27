import datetime
class Passenger:
    def __init__(self,
                 document_number: str,
                 name: str,
                 birthday: datetime,
                 phone: str,
                 money: int):
        self.document_number = document_number
        self.name = name
        self.birthday = birthday
        self.phone = phone
        self._money: int = money

    def use_money(self, count: int):
        self._money -= count

    def add_money(self, count: int):
        self._money += count

    def show_money(self):
        print(self._money)