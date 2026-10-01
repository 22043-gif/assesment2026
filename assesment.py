#Stella Jones
#02.09.2026
#Programming Assesment 
#“Waimak Build Co ” Quotation Creator

#Libraries 

#Imports module from Python's library, allowing for use of built-in classes and functions related to time
import datetime 
#Imports module from Python's library, allowing for reading and writing of json (JavaScript Object Notation) data
import json
#Imports a class from a Python model, lets the program create and manage file system paths as objects
from pathlib import Path


#Constants
#Creates a new object from the Path class, where quotes are saved
QUOTE_FILE = Path("quotes.json")

#Defines fixed prices and rates rather than using literals, easier to read, maintain, and update  
BASIC_KIT = 75000
TRADE_DISCOUNT_RATE = 0.1
GST = 0.15

#A nested dictionary holding upgrade options, and keys to their respective prices
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

#Stores upgrade option definitions rather than using literals, easier to read, maintain, and update  
BATH_OP_BASE = "Functional bathroom"
BATH_OP_ONE = "Tiled floor, spa bath, shower, tapware"

KITC_OP_BASE = "Fitted kitchen"
KITC_OP_ONE = "Unit/shelf upgrades and worktop"
KITC_OP_TWO = "As op 1, plus induction hob"
KITC_OP_THREE = "As op 1, plus Deluxe appliance pack"

LIVE_OP_BASE = "No appliances"
LIVE_OP_ONE = "TV point plus roof mounted aerial"
LIVE_OP_TWO = "TV point plus satellite dish"

HEATPUMP_LIVE = "4.5 KW"
HEATPUMP_BED = "2.5 KW"


#Classes

class Person:
    """Each object represents a customer in the quotation system.

    Collects/stores contact details to linked to a quote and 
    trade status to determine eligibility for trade discounts in final calculations.
    """    
    def __init__(self, name: str, phone: str, address: str, is_trade: bool):
        """
        Initialises a new instant of the class Person with their details
        
        Args:
            name (str): The full name of the custome
            phone (str): Contact phone number
            address (str): Personal or business address
            is_trade (bool): Indicating if the customer has a trade account 
                True for yes account/10% discount, False for no account/retail rate
        """
        #These take the values passed as parameters and save them as attributes inside object instance
        self.name = name
        self.phone = phone
        self.address = address
        self.is_trade = is_trade
    
class Quote:
    """Each object represents a quote in the system
    
    Handles pricing calculations based on option selection and prints a quote
    using said calculations for the user
    """
    def __init__(self, customer: Person, bathroom_option: int, 
                 kitchen_option: int, livingroom_option: int, heatpump_living: bool, 
                 heatpump_bedroom: bool, socket_1g_count: int, socket_2g_count: int,
                 network_points_count: int, ref_number: str = None):
        """
        Initialises a new instant of the class Quote with the users option slection and
        gentrates a refrance code

        Args:
            customer (Person): The Person object holding contact details and trade status.
            bathroom_option (int): Selected upgrade for bathroom 
            kitchen_option (int): Selected upgrade for kitchen 
            livingroom_option (int): Selected upgrade for living room 
            heatpump_living (bool): True if living room heat pump selected, fFalse otherwise
            heatpump_bedroom (bool): True if bedroom heat pump selected, False otherwise
            socket_1g_count (int): Number of additional 1G electrical sockets
            socket_2g_count (int): Number of additional 2G electrical sockets
            network_points_count (int): Number of additional network points 
            ref_number (str, optional): Pre-existing reference ID when loading saved quotes. Defaults to None.    
        """

        #Shows object aggregation as Quote class contains a reference to an object of Person class as an attribute
        self.customer = customer

        #Seting reference code
        #For loeading an existing quote, keeps orginal ref and sets as an attribute 
        if ref_number:
            self.ref_number = ref_number
        #Genrates new code quote not pulled from JSON file  
        else:
            #Sets varible equal to date in short format
            date_str = datetime.datetime.now().strftime("%d%m%Y")
            #Sets varible equal to 3 chacters, not spaces, in uppercase
            clean_name = customer.name.replace(" ", "")[:3].upper()
            #Sets varibles as attribute
            self.ref_number = (clean_name + date_str)
        
        #Takes options passed as parameters and saves them as attributes inside object instance
        self.bathroom_option = bathroom_option
        self.kitchen_option = kitchen_option
        self.livingroom_option = livingroom_option
        
        self.heatpump_living = heatpump_living
        self.heatpump_bedroom = heatpump_bedroom
        
        self.socket_1g_count = socket_1g_count
        self.socket_2g_count = socket_2g_count
        self.network_points_count = network_points_count

    def calculate_cost_upgrades(self) -> float:
        """
        Uses the object attributes/upgrade choices to calculate the cost of each upgrade made

        Returns: 
            float: Total sum of selected upgrades excluding base kit cost and GST.
        """
        #Local varible set to 0 to inticate that initial cost of upgrades $0
        total = 0.0

        #Room Upgrades
        #.get() searchs dictionary for room, then for a key matching selected option
        #It returns the associated value and adds it to total
        #If key doesn't exist, as no upgrade = 0, .get() returns set defult value 0.0
        #Total is now price of upgrades
        total += PRICES["bathroom"].get(self.bathroom_option, 0.0)
        total += PRICES["kitchen"].get(self.kitchen_option, 0.0)
        total += PRICES["livingroom"].get(self.livingroom_option, 0.0)

        #Heatpump upgrades
        #If bool value True, means a heatpump selected
        if self.heatpump_living:
            #Associated value from dict is added to total
            total += PRICES["heatpump_living"]
        #If false, nothing added to total
        if self.heatpump_bedroom:
            total += PRICES["heatpump_bedroom"]

        #Socket upgrades
        #Finds number of 1g sockets selected and muiples by associated value per socket
        #Added to total
        total += self.socket_1g_count * PRICES["socket_1g"]
        #Finds number of 2g sockets selected and muiples by associated value per socket
        #Added to total
        total += self.socket_2g_count * PRICES["socket_2g"]

        #Network upgrades
        #If user has selected additional points 
        if self.network_points_count > 0:
            #Mutiples amount selected by cost per point, then adds cost of network switch
            #Added to total
            total += (self.network_points_count * PRICES["network_point"]) + PRICES["network_switch"]
        #If there are no points added, no network switch added to total 

        #The total cost of the upgrades alone is returned 
        return total

    def calculate_total(self) -> dict:
        """Calculates all associated costs of the quote including GST, sub-total, and final total
        
        Returns:
            dict: Dictionary containing itemised costs('cost_upgrades', 'cost_gst', 
                  'initial_cost_of_build', 'discount_amount', 'final_total').
         """

        #Runs the previous method to calculate cost of upgrades and sets as attribute
        cost_upgrades = self.calculate_cost_upgrades()

        #Calculates initial cost by adding the base price to the upgrades 
        initial_cost_of_build = cost_upgrades + BASIC_KIT

        #Sets the discount to 0
        discount_amount = 0.0
        #If bool is True then is trade member 
        if self.customer.is_trade:
            #Discount calculated using member rate muitpled by the subtotal
            discount_amount = initial_cost_of_build * TRADE_DISCOUNT_RATE
            #If False then discount stays 0, no savings 
        
        #If bool is True then is trade member 
        if self.customer.is_trade:
            #The discounted upgrade total is calculated to show amount after discount applied 
            discounted_upgrades = cost_upgrades * (1 - TRADE_DISCOUNT_RATE)
        #If bool is False then is not trade member 
        else:
            #Then the discounted cost is not differnt as nothing removed 
            discounted_upgrades = cost_upgrades

        #Cost of GST is the discounted cost upgrades muitpled by rate
        #Base cost is already inclusive of GST and therefor not to be inclueded when calculating its cost 
        cost_gst = discounted_upgrades * GST

        #The final total is equal to upgrades + base price + GST - discount 
        final_total = initial_cost_of_build - discount_amount + cost_gst

        #A dictionary containing these amounts is returned to be used to produce a quote
        return {
            "cost_upgrades": cost_upgrades,
            "cost_gst": cost_gst,
            "initial_cost_of_build": initial_cost_of_build,
            "discount_amount": discount_amount,
            "final_total": final_total      
        }

    def object_to_dict(self) -> dict:
        """Converts the Quote instance into a dictionary format for JSON.

        Returns:
            dict: Structured dictionary containing all quote selections and final total.
        """

        #Runs previous method, setting it equal to a dictionary contain the costs of quote
        costs = self.calculate_total()
        
        #Returns a nested dictionary structure matching expected JSON schema
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
        """Prints/displays a completed quotation to the terminal console  """

        #Runs a method, setting it equal to a dictionary containing the costs of quote
        costs = self.calculate_total()

        #Section uses print staments to present a clear quote for user
        #Prints customer details, using items from costs dictionary 
        print("Thank you for using our quotation service, estimate incoming!\n")
        print("-" * 50)
        print("Waimak Build Co - Official Quote Estimation")
        print("-" * 50)
        print(f"Quote Refference Number:         {self.ref_number}")
        print(f"Customer Name:                   {self.customer.name}")
        print(f"Phone Number:                    {self.customer.phone}")
        print(f"Contact Address:                 {self.customer.address}")
        if self.customer.is_trade:
            print(f"Trade Account:                   Yes - 10% Discount")
        else: 
            print(f"Trade Account:                   No - 0% Discount")

        #Prints prices, to 2dp as is convention, using items from costs dictionary 
        print()
        print(f"Upgrades Subtotal (excl. GST): ${costs['cost_upgrades']:,.2f}")
        print(f"GST on Upgrades (15%):         ${costs['cost_gst']:,.2f}")
        print(f"Base Kit Cost:                 ${BASIC_KIT:,.2f}")
        #Only if trade member, else would be $0
        if self.customer.is_trade:
            print(f"Trade Discount Amount:        -${costs['discount_amount']:,.2f}")
        print()
        print(f"Total Estimate:                ${costs['final_total']:,.2f}")
        print("-" * 50)
        print()

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

#Validation functions

def get_valid_int(prompt: str, min_val: int = 0, max_val: int = None) -> int:
    """
    Prompts for integer input, continuously validates range constraints and data type

    Args:
        prompt(str): the text prompting user input
        min_val(int): the minimum acceptable integer value, default 0
        max_val(int): the minimum acceptable integer value

    Returns:
        int: a validated whole number that meets set constraints
    """
    #Loop will run continuously until vaild integer is entered
    while True:
        #User promted to enter number, leading/trailing white space removed 
        raw_input = input(prompt).strip()
        #Will attempt to convert to an integer data type
        try:
            val = int(raw_input)
            #Reject if value is lower than minumum 
            if val < min_val:
                #Given feedback
                print(f"Try again, value cannot be less than {min_val}.")
            #Reject if value is higher than maximum, if one is defined
            #If no maximum defined, not caught
            elif max_val is not None and val > max_val:
                print(f"Try again, value must be between {min_val} and {max_val}.")
            #Meets critera 
            else:
                #A validated integer is returned
                return val
        #Handles non-integer input like floats, letters, or special characters 
        #When produces an error, will catch, provide feedback and prompt again
        except ValueError:
            print("Try again, that was invalid input and not a whole number.")


def get_valid_string(prompt: str, field_name: str) -> str:
    """Ensures string text fields are not blank/whitespace only
    
    Args:
        prompt (str): text shown to the user to promt input
        field_name (str): field name used in validation error messages 

    Returns:
        str: non-empty string entered by the user
    """
    #Loop will run continuously until vaild text is entered
    while True:
        #User promted to enter text, leading/trailing white space removed 
        user_input = input(prompt).strip()
        #Will evaluate to True if non-empty in boolean checks
        if user_input:
            #Valid text is returned 
            return user_input
        #If evaluates to False, will give feedback because input was blank or only whitespa
        print(f"Try again, {field_name} cannot be left blank.")

def get_valid_bool(prompt: str) -> bool:
    """Validates yes/no user inpout and converts the string to a boolean value

    Args:
        prompt (str): text shown to the user to prompt input

    Returns:
        bool: True if user selects yes/y, False if user selects no/n
    """
    #Loop will run continuously until valid yes/no entered 
    while True:
        #User promted to enter y/n, leading/trailing white space removed, converet to lowercase
        choice = input(prompt).strip().lower()
        #If it is a postive input
        if choice in ["yes", "y"]:
            return True
        #If it is a postive input
        elif choice in ["no", "n"]:
            return False
        #If it is not a boolen value, feedback is given and loop will repeat
        print("Try again, that isn't an option.")


#Functions for input gathering     

def get_user_details() -> Person:
    """
    Prompts the user for customer contact information and trade status.

    Returns:
        Person: an instance of the Person class, object holding the customer's validated details.
    """
    print("Step 1. Please Enter Personal Details")
    name = get_valid_string("Name: ", "Name")
    phone = get_valid_string("Phone number: ", "Phone num") 
    address = get_valid_string("Address: ", "Address")
    is_trade = get_valid_bool("Are you a trade member (y/n): ")

    return Person(name, phone, address, is_trade)

def get_build_details():
    """
    This function will get user input on the details of what they want in their design
    """

    print("Step 2. Please Select any Upgrades to the Base Pack")

    print(f"""\nBathroom Options -  
    0: {BATH_OP_BASE},+$0
    1: {BATH_OP_ONE},+${PRICES['bathroom'][1]:,.2f}""")
    bathroom_option = get_valid_int("Select option (0 - 1): ", min_val=0, max_val=1)

    print(f"""\nKitchen Options -  
    0: {KITC_OP_BASE},+$0
    1: {KITC_OP_ONE},+${PRICES['kitchen'][1]:,.2f}
    2: {KITC_OP_TWO},+${PRICES['kitchen'][2]:,.2f}
    3: {KITC_OP_THREE},+${PRICES['kitchen'][3]:,.2f}""")
    kitchen_option = get_valid_int("Select option (0 - 3): ", min_val=0, max_val=3)

    print(f"""\nLiving Room Options-  
    0: {LIVE_OP_BASE},+$0
    1: {LIVE_OP_ONE},+${PRICES['livingroom'][1]:,.2f}
    2: {LIVE_OP_TWO},+${PRICES['livingroom'][2]:,.2f}""")
    livingroom_option = get_valid_int("Select option (0 - 2): ", min_val=0, max_val=2)

    print("\nHeatpumps - ")
    print (f"Would you like to add a {HEATPUMP_LIVE} heat pump in the living room?,+${PRICES['heatpump_living']:,.2f}?")
    heatpump_living = get_valid_bool("Select (y/n): ")

    print (f"Would you like to add a {HEATPUMP_BED} heat pump in the bedroom room?,+${PRICES['heatpump_bedroom']:,.2f}?")
    heatpump_bedroom = get_valid_bool("Select (y/n): ")

    print("\nSocket Upgrades - ")
    socket_1g_count = get_valid_int(f"Number of extra 1G sockets, ${PRICES['socket_1g']:,.2f} ea: ", min_val=0, max_val=12)
    remaining_allowed = 12 - socket_1g_count
    if remaining_allowed > 0:
        print(f"(You can add up to {remaining_allowed} extra 2G sockets)")
        socket_2g_count = get_valid_int(f"Number of extra 2G sockets, ${PRICES['socket_2g']:,.2f} ea: ", min_val=0, max_val=remaining_allowed)
    else:
        print(f"(Sorry, you cannot add any 2G as you have reached the maximum number of sockets")
        socket_2g_count = 0

    print("\nNetwork Upgrades - ")
    print ("Please note adding 2 or more network points, will mean a $100 switch is also added automatically")
    while True:
        network_points_count = get_valid_int("How many network points required? (0, or 2 - 8): ", min_val=0, max_val=8)
        if network_points_count == 1:
            print("Try again, you cannot select only 1 network point")
        else:
            break

    return bathroom_option, kitchen_option, livingroom_option, heatpump_living, heatpump_bedroom, socket_1g_count, socket_2g_count, network_points_count
           
#Function for returning stored data
def view_saved_quotes(quotes_data: list):
    """Description fo func"""
    if not quotes_data:
        print("\nNo  quotes found.")
        return

    print("SAVED QUOTES HISTORY ")
    for i, item in enumerate(quotes_data, start=1):
        cust = item["customer"]
        print(f"{i}. Ref: {item['ref_number']} | Name: {cust['name']} | Total: ${item['final_total']:,.2f}")


def main():
    quotes_data = load_quotes()

    while True:
        print("-" * 50)
        print("Welcome to the Waimak Build Co, Quotation Creator!")
        print("1. Create New Quote")
        print("2. View Saved Quotes Summary")
        print("3. Exit")
        print("-" * 50)
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            print("\n" + "-" * 50)
            print("Create New Quote")
            print("-" * 50)
            print()

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
        else:
            print("Sorry, that isn't an option we provide")


if __name__ == "__main__":
    main()