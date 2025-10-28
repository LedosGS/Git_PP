from typing import Dict
import os
import sys

class Page():
    def __init__(self, name: str):
        self.name: str = name
        self.actions = {Action("next" , )}



class Action():
    def __init__(self, name:str, action :lambda: ()):
        self.name: str = name
        self.action:lambda: () = action

    def use(self):
        return self.action()

    def __str__(self):
        return self.name
    
    
def home_page():
    print("введите [x] чтобы выйти")
    action = input(": ")
    if (action[0] == "x" or action[0] == "ч"):
        sys.exit()
    else:
        os.system("cls")
        home_page()