#Stella Jones
#02.09.2026
#Programming Assesment 
#“Waimak Build Co ” Quotation Creator

#Libraries 

#must add file

#Constants
from unicodedata import name


BASIC_KIT = 75000
TRADE_DISCOUNT_RATE = 0.1
GST = 0.15

BATHROOM_UPGRADE_A = 2500

KITCHEN_UPGRADE_A = 2000
KITCHEN_UPGRADE_B = 3500
KITCHEN_UPGRADE_C = 6000

LIVINGROOM_UPGRADE_A = 250
LIVINGROOM_UPGRADE_B = 250
LIVINGROOM_UPGRADE_C = 2500

BEDROOM_UPGRADE_A = 1800

ONE_G_SOCKET_PRICE = 40
TWO_G_SOCKET_PRICE = 50
NETWORK_SWITCH_PRICE = 100
NETWORK_POINT_PRICE = 50

#Dictoinaries
people = []

class Person:
    def __init__(self, name, phone, address, discount):
        self.name = name
        self.phone = int(phone)
        self.address = address
        self.discount = discount

    def introduce(self):
                print(f"Hi, my name is {self.name}.")
                print(f"My phone number is {self.phone}.")

def user_details():
    """
    Finds names
    """
    print("Welcome to the Waimak Build Co, Quotation Creator!")
    name = input("Name: ")
    phone = input("Phone number: ") 
    address = input("Address: ")

    applied__loop = True
    while applied__loop:
        trade_member = input("Are you a trade member (yes/no): ")
        if trade_member == "yes":
            print("You are eligible for a discount")
            applied__loop = False
        elif trade_member == "no":
            print("You are not eligible for a discount")
            applied__loop = False
        else:
            print("Please enter yes or no")
    


        new_person = Person(name, phone, address, trade_member)
        new_person.introduce()

def build_details():
    """
    This function will get user input on the details of what they want in their design
     """
    
    upgrade_loop = True
    upgrade = input("Would you like to add upgrades to the basic kit (yes/no): ")
    while upgrade_loop:
        if upgrade == "yes":
            print("Here are the upgrades available:")
            print("basic: no added \n" + "costupgrade:")

            upgrade = input("Do you want to add another one?")
        elif upgrade == "no":
            print("No upgrades for you!")
            upgrade_loop = False
        else:
            upgrade = input("Please enter yes or no")

    
    


"""
def calculations():
This function will use input from build_details to calculate the total cost of the build
build_details()
put in class


 """

build_details()