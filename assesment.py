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
BATHROOM_DEFAULT_D = 0

KITCHEN_UPGRADE_A = 2000
KITCHEN_UPGRADE_B = 3500
KITCHEN_UPGRADE_C = 6000
KITCHEN_DEFAULT_D = 0

LIVINGROOM_UPGRADE_A = 250
LIVINGROOM_UPGRADE_B = 250
LIVINGROOM_DEFAULT_D = 0

HEATPUMP_LIVINGROOM = 2500
HEATPUMP_BEDROOM = 1800
HEATPUMP_DEFAULT_D = 0

ONE_G_SOCKET_PRICE = 40
TWO_G_SOCKET_PRICE = 50
NETWORK_SWITCH_PRICE = 100
NETWORK_POINT_PRICE = 50

#Dictoinaries
people = []

class Person:
    def __init__(self, name, phone, address, discount, bathroom_option, kitchen_option, livingroom_option, heatpump_option):
        self.name = name
        self.phone = int(phone)
        self.address = address
        self.discount = discount
        self.bathroom_option = bathroom_option
        self.kitchen_option = kitchen_option
        self.livingroom_option = livingroom_option
        self.heatpump_option = heatpump_option

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

        return(name, phone, address, trade_member)


def build_details():
    """
    This function will get user input on the details of what they want in their design
     """
    print("Here are the upgrades available:")
    print("Bathroom - \n    Basic: no added cost \n    Upgrade A: an aditional $2500")
    bathroom_option = input("    Please select default (d) or upgrade (a): ")
    print("Kitchen - \n    Basic: no added cost \n    Upgrade A: an aditional $2000 \n    Upgrade B: an aditional $3500 \n    Upgrade C: an aditional $6000")
    kitchen_option = input("    Please select default (d) or upgrade (a) or (b) or (c): ")
    print("Living Room - \n    Basic: no added cost \n    Upgrade A: an aditional $250 \n    Upgrade B: an aditional $250")
    livingroom_option = input("    Please select default (d) or upgrade (a) or (b): ")
    print("Heat Pumps - \n    Living Room: an aditional $2500 \n    Bedroom: an aditional $1800")
    heatpump_option = input("    Please select none (d), living room (a), bedroom (b) or both (c): ")

    return(bathroom_option, kitchen_option, livingroom_option, heatpump_option)

def network_details():
    add_socket = input("Would you like to add an addtional socket? (y/n)")
    while add_socket != ("y") or ("n"):
        if add_socket == ("y"):
            add_socket = True
        elif add_socket == ("n"):
            add_socket = False
        else:
            add_socket = input("Would you like to add an addtional socket? (y/n)")         
         
"""

def prices(bathroom_option, kitchen_option, livingroom_option, heatpump_option):
    if bathroom_option == "a":
        bathroom_cost = BATHROOM_UPGRADE_A
    else:
        bathroom_cost = BATHROOM_DEFAULT_D

    if kitchen_option == "a":
        kitchen_cost = KITCHEN_UPGRADE_A
    elif kitchen_option == "b":
        kitchen_cost = KITCHEN_UPGRADE_B
    elif kitchen_option == "c":
        kitchen_cost = KITCHEN_UPGRADE_C
    else:
        kitchen_cost = KITCHEN_DEFAULT_D

    if livingroom_option == "a":
        livingroom_cost = LIVINGROOM_UPGRADE_A
    elif livingroom_option == "b":
        livingroom_cost = LIVINGROOM_UPGRADE_B
    else:
        livingroom_cost = LIVINGROOM_DEFAULT_D

    if heatpump_option == "a":
        heatpump_cost = HEATPUMP_LIVINGROOM
    elif heatpump_option == "b":
        heatpump_cost = HEATPUMP_BEDROOM
    elif heatpump_option == "c":
        heatpump_cost = HEATPUMP_LIVINGROOM + HEATPUMP_BEDROOM
    else:
        heatpump_cost = HEATPUMP_DEFAULT_D


def statements(bathroom_option, bathroom_cost, kitchen_option, kitchen_cost, livingroom_option, livingroom_cost, heatpump_option, heatpump_cost):
    print("Here is your personilized quotation based on your selections:")
    print (f"Basic Kit: ${BASIC_KIT}")
    print (f"Additional Upgrades:")
    if bathroom_cost > 0:
        print(f"You selected Option {bathroom_option}")
        print(f"   Bathroom:${bathroom_cost}")
    if kitchen_cost > 0:
        print(f"You selected Option {kitchen_option}")
        print(f"   Kitchen: ${kitchen_cost}")
    if livingroom_cost > 0:
        print(f"You selected Option {livingroom_option}")
        print(f"   Living Room: ${livingroom_cost}")
    if heatpump_cost > 0:
        print(f"You selected Option {heatpump_option}")
        print(f"   Heat Pumps: ${heatpump_cost}")
    if bathroom_cost == 0 and kitchen_cost == 0 and livingroom_cost == 0 and heatpump_cost == 0:
        print("   No additional upgrades selected")
    
"""

name, phone, address, trade_member = user_details()
bathroom_option, kitchen_option, livingroom_option, heatpump_option = build_details()

new_person = Person(name, phone, address, trade_member, bathroom_option, kitchen_option, livingroom_option, heatpump_option)


introduce = new_person.introduce()