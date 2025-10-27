import datetime
class Passenger:
    def __init__(self,
                 document_number: str,
                 name: str,
                 birthday: datetime,
                 phone: str,
                 money: int):
        self.document_number: str = document_number
        self.name: str = name
        self.birthday: str = str(birthday)
        self.phone: str = phone
        self._money: int = money

    def use_money(self, count: int):
        self._money -= count

    def add_money(self, count: int):
        self._money += count

    def show_money(self):
        print(self._money)

    def get_money(self):
        return self._money

    def serialize(self):
        return {"document_number": self.document_number,
                "name": self.name,
                "birthday": self.birthday,
                "phone": self.phone,
                "money": self._money}

    def show_passenger_info(self):
        print(f'name: {self.name}\n'
              f'document number: {self.document_number}\n'
              f'birthday date: {self.birthday}\n'
              f'phone number: {self.phone}\n'
              f'wallet money: {self._money}\n')