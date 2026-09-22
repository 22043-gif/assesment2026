#Stella Jones
#02.09.2026
#Programming Assesment 
#“Waimak Build Co ” Quotation Creator

#Libraries 

#must add file

import datetime 


#----------
#Constants
#----------

BASIC_KIT = 75000
TRADE_DISCOUNT_RATE = 0.1
GST = 0.15

PRICES = {
    "bathroom": {1: 2500.0},
    "kitchen": {1: 2000.0, 2: 3500.0, 3: 6000.0},
    "livingroom": {1: 250.0, 2: 250.0},
    "heatpump_living": 2500.0,
    "heatpump_bedroom": 1800.0,
    "socket_1g": 40.0,
    "socket_2g": 50.0,
    "network_point": 50.0,
    "network_switch": 100.0
}


#----------
#Classes
#----------

class Person:
    """Stores cust details"""
    def __init__(self, name, phone, address, is_trade):
        self.name = name
        self.phone = phone
        self.address = address
        self.is_trade = is_trade

class Quote:
    """Handles option selections, pring calc and quote printing """
    def __init__(self, customer: Person, bathroom_option, 
                 kitchen_option, livingroom_option, heatpump_living, 
                 heatpump_bedroom, socket_1g_count, socket_2g_count,
                 network_points_count):

        self.customer = customer
        date_str = datetime.datetime.now().strftime("%d%m%Y")
        self.ref_number = f"{customer.name[:3]}-{date_str}"
        
        self.bathroom_option = bathroom_option
        self.kitchen_option = kitchen_option
        self.livingroom_option = livingroom_option
        
        self.heatpump_living = heatpump_living
        self.heatpump_bedroom = heatpump_bedroom
        
        self.socket_1g_count = socket_1g_count
        self.socket_2g_count = socket_2g_count
        self.network_points_count = network_points_count

        #Other functions in class
        
        def calculate_cost_upgrades(self) -> float:
            total = 0.0

            #Room upgrades
            total += PRICES["bathroom"].get(self.bathroom_opt, 0.0)
            total += PRICES["kitchen"].get(self.kitchen_opt, 0.0)
            total += PRICES["livingroom"].get(self.living_opt, 0.0)

            #Heatpump upgrades
            if self.heatpump_living:
                total += PRICES["heatpump_living"]
            if self.heatpump_bedroom:
                total += PRICES["heatpump_bedroom"]

            #Socket upgrades
            total += self.socket_1g_count * PRICES["socket_1g"]
            total += self.socket_2g_count * PRICES["socket_2g"]

            #Network upgrades
            if self.network_points_count > 0:
                total += (self.network_points_count * PRICES["network_point"]) + PRICES["network_switch"]

            return total

        def calculate_total(self) -> dict:

            cost_upgrades = self.calculate_cost_upgrades
            cost_gst = cost_upgrades * GST
            total_cost_upgrades = cost_upgrades + cost_gst

            initial_cost_of_build = total_cost_upgrades + BASIC_KIT

            discount_amount = 0.0

            if self.customer.is_trade:
                discount_amount = initial_cost_of_build * TRADE_DISCOUNT_RATE

            final_total = initial_cost_of_build - discount_amount

            return {
                "cost_upgrades": cost_upgrades,
                "cost_gst": cost_gst,
                "total_cost_upgrades": total_cost_upgrades,
                "initial_cost_of_build": initial_cost_of_build,
                "discount_amount": discount_amount,
                "final_total": final_total      
            }

        def display_quote(self):
            """Displaying quote for user on console"""

            costs = self.calculate_total()

            #Display details of user

            print("    Thank you for using our quotation service, estimate incoming!")
            print("\n")
            print("Waimak Build Co - Official Quote")
            print("\n")
            print(f"Quote Refference Number:         {self.ref_number}")
            print(f"Customer Name:                   {self.customer.name}")
            print(f"Phone Number:                    {self.customer.phone}")
            print(f"Contact Address:                 {self.customer.address}")
            if self.customer.is_trade:
                print(f"Trade Account:                   Yes - 10% Discount")
            else: 
                print(f"Trade Account:                   No - 0% Discount")

            #Display Upgrade Details



    def introduce(self):
                print(f"Hi, my name is {self.name}.")
                print(f"My phone number is {self.phone}.")


def get_user_details():
    """
    Finds names
    """
    print("Welcome to the Waimak Build Co, Quotation Creator!")
    name = input("Name: ")
    phone = input("Phone number: ") 
    address = input("Address: ")

    applied__loop = True
    while applied__loop:
        is_trade = input("Are you a trade member (yes/no): ")
        if is_trade == "yes":
            print("You are eligible for a discount")
            applied__loop = False
        elif is_trade == "no":
            print("You are not eligible for a discount")
            applied__loop = False
        else:
            print("Please enter yes or no")

    return(name, phone, address, is_trade)


def get_build_details():
    """
    This function will get user input on the details of what they want in their design
     """

    #Gets room upgrades
    print("Here are the upgrades available:")
    print("Bathroom - \n    Basic: no added cost \n    Upgrade 1: an aditional $2500")
    bathroom_option = input("    Select default (0 / 1): ")

    print("Kitchen - \n    Basic: no added cost \n    Upgrade 1: an aditional $2000 \n    Upgrade 2: an aditional $3500 \n    Upgrade 3: an aditional $6000")
    kitchen_option = input("    Selct default (0 / 1 / 2 / 3): ")

    print("Living Room - \n    Basic: no added cost \n    Upgrade A: an aditional $250 \n    Upgrade B: an aditional $250")
    livingroom_option = input("    Please select default (0 / 1 / 2): ")

    heatpump_living = input("\nAdd 4.5kW Living Room Heat Pump? (+$2,500) (y/n): ").strip().lower() == "y"
    heatpump_bedroom = input("Add 2.5kW Bedroom Heat Pump? (+$1,800) (y/n): ").strip().lower() == "y"

    #Get network details 

    socket_1g_count = int(input("\nHow many extra 1G sockets?: "))
    socket_2g_count = int(input("How many extra 2G sockets?: "))  

    network_points_count = int(input("How many network points?: "))

    return bathroom_option, kitchen_option, livingroom_option, heatpump_living, heatpump_bedroom, socket_1g_count, socket_2g_count, network_points_count
           

   
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


user = get_user_details()
bathroom_option, kitchen_option, livingroom_option, heatpump_living, heatpump_bedroom, socket_1g_count, socket_2g_count, network_points_count = get_build_details()

new_quote = Quote(user,bathroom_option, kitchen_option, livingroom_option, heatpump_living, heatpump_bedroom, socket_1g_count, socket_2g_count, network_points_count)
quote.display_quote()


