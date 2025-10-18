import uuid
from enum import Enum, unique


class Person:

    def __init__(self, person_name, person_birthday, person_gender, person_phone):
        self.__name: str = person_name
        self.__birthday: Date = person_birthday
        self.__gender: Gender = person_gender
        self.__phone: Phone = person_phone

    def get_name(self): return self.__name

    def get_birthday(self): return self.__birthday

    def get_gender(self): return self.__gender

    def get_phone(self): return self.__phone

    def set_name(self, person_name): self.__name = person_name

    def set_birthday(self, person_birthday): self.__birthday = person_birthday

    def set_gender(self, person_gender): self.__gender = person_gender

    def set_phone(self, person_phone): self.__phone = person_phone


class User(Person):

    def __init__(self, *args, **kwargs):
        if len(args) == 2 and isinstance(args[0], Person):

            person, email = args
            super().__init__(
                person.get_name(),
                person.get_birthday(),
                person.get_gender(),
                person.get_phone()
            )
            self.__email = email
        else:

            if len(args) == 5:
                person_name, person_birthday, person_gender, person_phone, email = args
            else:

                person_name = kwargs.get('person_name')
                person_birthday = kwargs.get('person_birthday')
                person_gender = kwargs.get('person_gender')
                person_phone = kwargs.get('person_phone')
                email = kwargs.get('email')

            super().__init__(person_name, person_birthday, person_gender, person_phone)
            self.__email = email

        self.__id = uuid.uuid4()
        self.__tickets = []


    def get_email(self): return self.__email

    def get_id(self): return self.__id

    def get_tickets(self): return self.__tickets

    def set_email(self, email): self.__email = email

    def add_ticket(self): pass


@unique
class Months(Enum):
    JANUARY = 0
    FEBRUARY = 1
    MARCH = 2
    APRIL = 3
    MAY = 4
    JUNE = 5
    JULY = 6
    AUGUST = 7
    SEPTEMBER = 8
    OCTOBER = 9
    NOVEMBER = 10
    DECEMBER = 11


@unique
class Gender(Enum):
    MALE = 0
    FEMALE = 1


class Date:
    def __init__(self, day=1, month=Months.JANUARY, year=2025):
        self.day = day  # int
        self.month = month  # Months
        self.year = year  # int


class Phone:
    def __init__(self, number="+89150000001"):
        self.number = number


birthday = Date(10, Months.MARCH, 2007)
pers = Person("Naletov Artem", birthday, Gender.MALE, Phone())
usr = User(pers, "Artem1000@gmail.com")
print(usr.get_email())
