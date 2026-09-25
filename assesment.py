#Stella Jones
#02.09.2026
#Programming Assesment 
#“Waimak Build Co ” Quotation Creator

#Libraries 

#must add file

import datetime 
import json
from pathlib import Path


#Constants

QUOTE_FILE = Path("quotes.json")

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


#Classes

class Person:
    """Stores cust details"""
    def __init__(self, name, phone, address, is_trade):
        self.name = name
        self.phone = phone
        self.address = address
        self.is_trade = is_trade

    def introduce(self):
        print("Hello!" + self.name)

class Quote:
    """Handles option selections, pricing calculations and quote printing """
    def __init__(self, customer: Person, bathroom_option: int, 
                 kitchen_option: int, livingroom_option: int, heatpump_living: bool, 
                 heatpump_bedroom: bool, socket_1g_count: int, socket_2g_count: int,
                 network_points_count: int, ref_number: str = None):


        self.customer = customer

        #Reference number

        if ref_number:
            self.ref_number = ref_number
        else:
            date_str = datetime.datetime.now().strftime("%d%m%Y")
            clean_name = customer.name.replace(" ", "")[:3].upper()
            self.ref_number = (clean_name + date_str)
        
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
        """This is decription for func"""
        total = 0.0

        #Room upgrades
        total += PRICES["bathroom"].get(self.bathroom_option, 0.0)
        total += PRICES["kitchen"].get(self.kitchen_option, 0.0)
        total += PRICES["livingroom"].get(self.livingroom_option, 0.0)

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
        """This is purpose of function"""

        cost_upgrades = self.calculate_cost_upgrades()
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

    def object_to_dict(self) -> dict:
        """Explain purpose of function"""

        costs = self.calculate_total()
        
        return {
            "ref_number": self.ref_number,
            "customer": {
                "name": self.customer.name,
                "phone": self.customer.phone,
                "address": self.customer.address,
                "is_trade": self.customer.is_trade
            },
            "options": {
                "bathroom_option": self.bathroom_option,
                "kitchen_option": self.kitchen_option,
                "livingroom_option": self.livingroom_option,
                "heatpump_living": self.heatpump_living,
                "heatpump_bedroom": self.heatpump_bedroom,
                "socket_1g_count": self.socket_1g_count,
                "socket_2g_count": self.socket_2g_count,
                "network_points_count": self.network_points_count
            },
            "final_total": costs["final_total"]
        }






    def display_quote(self):
        """Displaying quote for user on console"""

        costs = self.calculate_total()

        #Display details of user

        print("Thank you for using our quotation service, estimate incoming!")
        print()
        print("-" * 50)
        print("Waimak Build Co - Official Quote")
        print("-" * 50)
        print(f"Quote Refference Number:         {self.ref_number}")
        print(f"Customer Name:                   {self.customer.name}")
        print(f"Phone Number:                    {self.customer.phone}")
        print(f"Contact Address:                 {self.customer.address}")
        if self.customer.is_trade:
            print(f"Trade Account:                   Yes - 10% Discount")
        else: 
            print(f"Trade Account:                   No - 0% Discount")

        #Display Upgrade Details
        print()
        print(f"Upgrades Subtotal (excl. GST): ${costs['cost_upgrades']:,.2f}")
        print(f"GST on Upgrades (15%):         ${costs['cost_gst']:,.2f}")
        print(f"Base Kit Cost:                 ${BASIC_KIT:,.2f}")
        if self.customer.is_trade:
            print(f"Trade Discount Amount:        -${costs['discount_amount']:,.2f}")
        print()
        print(f"TOTAL ESTIMATE:                ${costs['final_total']:,.2f}")
        print("-" * 50)

#Functions

#File functions
def load_quotes() -> list:
    """Description of func."""
    if QUOTE_FILE.exists():
        with open(QUOTE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    return []

def save_quotes(quotes_data: list):
    """Discription of func"""
    with open(QUOTE_FILE, "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, indent=2)

#Punctions for input gathering
        

def get_user_details() -> Person:
    """
    Finds all the names and infomation not directly involved in calculations
    """
    print("Welcome to the Waimak Build Co, Quotation Creator!")
    name = input("Name: ")
    phone = input("Phone number: ") 
    address = input("Address: ")


    trade_choice = input("Are you a trade member (yes/no): ").strip().lower()
    is_trade = (trade_choice == "yes")


    return Person(name, phone, address, is_trade)



def get_build_details():
    """
    This function will get user input on the details of what they want in their design
     """

    #Gets room upgrades
    print("Here are the upgrades available:")
    print("Bathroom - \n    Basic: no added cost \n    Upgrade 1: an aditional $2500")
    bathroom_option = int(input("    Select default (0) / (1): "))

    print("Kitchen - \n    Basic: no added cost \n    Upgrade 1: an aditional $2000 \n    Upgrade 2: an aditional $3500 \n    Upgrade 3: an aditional $6000")
    kitchen_option = int(input("    Selct default (0) / (1) / (2) / (3)): "))

    print("Living Room - \n    Basic: no added cost \n    Upgrade A: an aditional $250 \n    Upgrade B: an aditional $250")
    livingroom_option = int(input("    Please select default (0) / (1) / (2): "))

    print("Heatpumps - ")
    heatpump_living = input("    Add 4.5kW Living Room Heat Pump? (+$2,500) \n    Please select(y/n): ").strip().lower() == "y"
    heatpump_bedroom = input("    Add 2.5kW Bedroom Heat Pump? (+$1,800) \n    Please select(y/n): ").strip().lower() == "y"

    #Get network details 

    print("Network - ")
    socket_1g_count = int(input("\nHow many extra 1G sockets?: "))
    socket_2g_count = int(input("How many extra 2G sockets?: "))  

    network_points_count = int(input("How many network points?: "))

    return bathroom_option, kitchen_option, livingroom_option, heatpump_living, heatpump_bedroom, socket_1g_count, socket_2g_count, network_points_count
           
#Function for returning stored data
def view_saved_quotes(quotes_data: list):
    """Description fo func"""
    if not quotes_data:
        print("\nNo  quotes found.")
        return

    print("SAVED QUOTES HISTORY")
    for i, item in enumerate(quotes_data, start=1):
        cust = item["customer"]
        print(f"{i}. Ref: {item['ref_number']} | Name: {cust['name']} | Total: ${item['final_total']:,.2f}")



def main():
    quotes_data = load_quotes()

    while True:
        print("-" * 50)
        print("Waimak Build Co - Quote System")
        print("1. Create New Quote")
        print("2. View Saved Quotes Summary")
        print("3. Exit")
        print("-" * 50)
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            customer = get_user_details()
            
            (bathroom_option, 
             kitchen_option, 
             livingroom_option, 
             heatpump_living, 
             heatpump_bedroom, 
             socket_1g_count, 
             socket_2g_count, 
             network_points_count) = get_build_details()

            new_quote = Quote(customer, 
                              bathroom_option, 
                              kitchen_option, 
                              livingroom_option, 
                              heatpump_living, 
                              heatpump_bedroom, 
                              socket_1g_count, 
                              socket_2g_count, 
                              network_points_count)
            
            new_quote.display_quote()

            quotes_data.append(new_quote.object_to_dict())
            save_quotes(quotes_data)
            print("Quote successfully saved to file!")

        elif choice == "2":
            view_saved_quotes(quotes_data)

        elif choice == "3":
            print("\nThank you for using Waimak Build Co Quotation Creator. Goodbye!")
            break


if __name__ == "__main__":
    main()