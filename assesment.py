#Stella Jones
#02.09.2026
#Programming Assessment 
#“Waimak Build Co ” Quotation Creator

#V2

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
END = ["c", "cancel"]

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
        Initialises a new instance of the class Person with their details
        
        Args:
            name (str): The full name of the customer
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
        Initialises a new instant of the class Quote with the users option selection and
        generates a reference code

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

        #Setting reference code
        #For loading an existing quote, keeps original ref and sets as an attribute 
        if ref_number:
            self.ref_number = ref_number
        #Generates new code quote not pulled from JSON file  
        else:
            #Sets variable equal to date in short format
            date_str = datetime.datetime.now().strftime("%d%m%Y")
            #Sets variable equal to 3 characters, not spaces, in uppercase
            clean_name = customer.name.replace(" ", "")[:3].upper()
            #Sets variables as attribute
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
        #Local variable set to 0 to indicate that initial cost of upgrades $0
        total = 0.0

        #Room Upgrades
        #.get() searchs dictionary for room, then for a key matching selected option
        #It returns the associated value and adds it to total
        #If key doesn't exist, as no upgrade = 0, .get() returns set default value 0.0
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
        #Finds number of 1g sockets selected and multiplies by associated value per socket
        #Added to total
        total += self.socket_1g_count * PRICES["socket_1g"]
        #Finds number of 2g sockets selected and multiplies by associated value per socket
        #Added to total
        total += self.socket_2g_count * PRICES["socket_2g"]

        #Network upgrades
        #If user has selected additional points 
        if self.network_points_count > 0:
            #Multiplies amount selected by cost per point, then adds cost of network switch
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

        #If bool is True then is trade member 
        if self.customer.is_trade:
            #Discount calculated using member rate multiplied by the subtotal
            discount_amount = initial_cost_of_build * TRADE_DISCOUNT_RATE
            #The discounted upgrade total is calculated to show amount after discount applied 
            discounted_upgrades = cost_upgrades * (1 - TRADE_DISCOUNT_RATE)

        #If False then discount stays 0, no savings 
        else:
            discount_amount = 0.0
            #Then the discounted cost is not differnt as nothing removed 
            discounted_upgrades = cost_upgrades

        #Cost of GST is the discounted cost upgrades multiplied by rate
        #Base cost is already inclusive of GST and therefore not to be included when calculating its cost 
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

        #Header
        print("Thank you for using our quotation service, estimate incoming!\n")
        print("-" * 50)
        print("Waimak Build Co - Official Quote Estimation")
        print("-" * 50)

        #Personal details
        print("Personal details")
        print("-" * 30)
        print(f"Quote Reference Number:          {self.ref_number}")
        print(f"Customer Name:                   {self.customer.name}")
        print(f"Phone Number:                    {self.customer.phone}")
        print(f"Contact Address:                 {self.customer.address}")

        if self.customer.is_trade:
            print(f"Trade Account:                   Yes - 10% Discount")
        else: 
            print(f"Trade Account:                   No - 0% Discount")

        #Selected options
        print("\nSelected Upgrades")
        print("-" * 30)

        print(f"Bathroom:                        Option {self.bathroom_option}")
        print(f"Kitchen:                         Option {self.kitchen_option}")
        print(f"Living Room:                     Option {self.livingroom_option}")

        # Heat pumps
        if self.heatpump_living:
            print("Living Room Heat Pump:           Yes")
        else:
            print("Living Room Heat Pump:           No")

        if self.heatpump_bedroom:
            print("Bedroom Heat Pump:               Yes")
        else:
            print("Bedroom Heat Pump:               No")

        # Sockets
        print(f"Extra 1G Sockets:                x {self.socket_1g_count}")
        print(f"Extra 2G Sockets:                x {self.socket_2g_count}")

        # Network
        if self.network_points_count > 0:
            print(f"Network Points:                  x {self.network_points_count} + switch")
        else:
            print("Network Points:                   0")

        #Cost summary
        print("\nCost Summary - ")
        print("-" * 30)
        print(f"Upgrades Subtotal (excl. GST):   ${costs['cost_upgrades']:,.2f}")
        print(f"GST on Upgrades (15%):           ${costs['cost_gst']:,.2f}")
        print(f"Base Kit Cost:                   ${BASIC_KIT:,.2f}")
        #Only if trade member, else would be $0
        if self.customer.is_trade:
            print(f"Trade Discount Amount:          -${costs['discount_amount']:,.2f}")
        print()
        print(f"Total Estimate:                  ${costs['final_total']:,.2f}")
        print("-" * 50)

#Functions

#File functions
def load_quotes() -> list:
    """Reads saved quote records from the JSON file, if it exists

    Returns:
        list: A list of dictionaries (quotes) loaded from file, or an empty list if no file exists"""
    #Checks if the target file exists on the path before attempting to open
    if QUOTE_FILE.exists():
        #File is attempted to be opened in read mode safely
        #r to ensure file is Read, not overwritten
        try:
            with open(QUOTE_FILE, "r", encoding="utf-8") as f:
                #JSON file contents parsed to Python list of dictionaries
                #Returned for user
                return json.load(f)
        #If the file contains empty files, half-written JSON, or corrupted data it can prevent file from being read
        #This will catch errors produced and return empty lst rather than crashing
        except (json.JSONDecodeError, OSError):
            print("Issue with reading quotes file, starting with empty list")
            return []

    #Return an empty list if the file does not exist, like first run
    return []

def save_quotes(quotes_data: list):
    """Writes the current list of quote dictionaries to JSON file for storage

    Args:
        quotes_data (list): The list of quote dictionaries to be stored persistently"""
    #File is opened in Write mode with with utf-8 encoding
    with open(QUOTE_FILE, "w", encoding="utf-8") as f:
        #List to JSON file, formatted with a 2-space indentation
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
    #Loop will run continuously until valid integer is entered
    while True:
        #User prompted to enter number, leading/trailing white space removed 
        raw_input = input(prompt).strip()

        #User wants to exit
        if raw_input.lower() in END:
            return None
        
        #Will attempt to convert to an integer data type
        try:
            val = int(raw_input)
            #Reject if value is lower than minimum 
            if val < min_val:
                #Given feedback
                print(f"Try again, value cannot be less than {min_val}.")
            #Reject if value is higher than maximum, if one is defined
            #If no maximum defined, not caught
            elif max_val is not None and val > max_val:
                print(f"Try again, value must be {min_val} >/= and </= {max_val}.")
            #Meets criteria 
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
        prompt (str): text shown to the user to prompt input
        field_name (str): field name used in validation error messages 

    Returns:
        str: non-empty string entered by the user
    """
    #Loop will run continuously until valid text is entered
    while True:
        #User prompted to enter text, leading/trailing white space removed 
        user_input = input(prompt).strip()

        #User wants to exit
        if user_input.lower() in END:
            return None

        #Will evaluate to True if non-empty in boolean checks
        if user_input:
            #Valid text is returned 
            return user_input
        #If evaluates to False, will give feedback because input was blank or only whitespace
        print(f"Try again, {field_name} cannot be left blank.")

def get_valid_bool(prompt: str) -> bool:
    """Validates yes/no user input and converts the string to a boolean value

    Args:
        prompt (str): text shown to the user to prompt input

    Returns:
        bool: True if user selects yes/y, False if user selects no/n
    """
    #Loop will run continuously until valid yes/no entered 
    while True:
        #User prompted to enter y/n, leading/trailing white space removed, convert to lowercase
        choice = input(prompt).strip().lower()

        #User wants to exit
        if choice in END:
            return None

        #If it is a positive input
        if choice in ["yes", "y"]:
            return True
        #If it is a positive input
        elif choice in ["no", "n"]:
            return False
        #If it is not a boolean value, feedback is given and loop will repeat
        print("Try again, that isn't an option.")


#Functions for input gathering     

def get_user_details() -> Person:
    """
    Prompts the user for customer contact information and trade status.

    Returns:
        Person: an instance of the Person class, object holding the customer's validated details.
    """
    print("\nStep 1. Please Enter Personal Details") 
    print("-" * 30)
    print("Enter c/cancel at any time to end your quote")
    #Calls the string validation function with the prompt and field name 
    #Once valid text is entered set equal to variable
    name = get_valid_string("Name: ", "Name")
    #Catches when users want to exit quote, validation returns none
    if name is None:
        return None

    phone = get_valid_string("Phone number: ", "Phone num")
    if phone is None:
        return None
 
    address = get_valid_string("Address: ", "Address")
    if address is None:
        return None

    #Calls the boolean validation variable with the prompt and field name 
    #Once valid value is entered, varible set to True or False
    is_trade = get_valid_bool("Are you a trade member (y/n): ")
    if is_trade is None:
        return None

    print()

    #Returns the personal details to be stored in a quote  
    return Person(name, phone, address, is_trade)

def get_build_details() -> tuple:
    """
    Prompts the user to select room options, heat pumps, sockets, and network points.

    Displays formatted upgrade pricing fetched directly from defined global constants.

    Returns:
        tuple: A tuple containing all the user's selected options and amounts:
               (bathroom_option, kitchen_option, livingroom_option, 
                heatpump_living, heatpump_bedroom, socket_1g_count, 
                socket_2g_count, network_points_count)
    """

    print("Step 2. Please Select any Upgrades to the Base Pack")
    print("-" * 30)
    print("Enter c/cancel at any time to end your quote")
    #This multiline string will display all options for the bathroom
    #Using global constants and dictionary to give descriptions and prices  
    print(f"""Bathroom Options -  
0: {BATH_OP_BASE}, +$0
1: {BATH_OP_ONE}, +${PRICES['bathroom'][1]:,.2f}""")
    #Uses validation function to get an valid integer, corresponding to a bathroom option 
    bathroom_option = get_valid_int("Select option (0 - 1): ", min_val=0, max_val=1)
    if bathroom_option is None:
        return None

    #This multiline string will display all options for the kitchen
    #Using global constants and dictionary to give descriptions and prices  
    print(f"""\nKitchen Options -  
0: {KITC_OP_BASE}, +$0
1: {KITC_OP_ONE}, +${PRICES['kitchen'][1]:,.2f}
2: {KITC_OP_TWO}, +${PRICES['kitchen'][2]:,.2f}
3: {KITC_OP_THREE}, +${PRICES['kitchen'][3]:,.2f}""")
    #Uses validation function to get a valid integer, corresponding to a kitchen option 
    kitchen_option = get_valid_int("Select option (0 - 3): ", min_val=0, max_val=3)
    if kitchen_option is None:
        return None
    
    #This multiline string will display all options for the living room
    #Using global constants and dictionary to give descriptions and prices  
    print(f"""\nLiving Room Options -  
0: {LIVE_OP_BASE}, +$0
1: {LIVE_OP_ONE}, +${PRICES['livingroom'][1]:,.2f}
2: {LIVE_OP_TWO}, +${PRICES['livingroom'][2]:,.2f}""")
    #Uses validation function to get an integer, corresponding to a livingroom option 
    livingroom_option = get_valid_int("Select option (0 - 2): ", min_val=0, max_val=2)
    if livingroom_option is None:
        return None

    print("\nHeatpumps - ")

    #Using global constants and dictionary to give a description and price  
    print (f"Would you like to add a {HEATPUMP_LIVE} heatpump in the living room? +${PRICES['heatpump_living']:,.2f}?")
    #Uses validation function to get a boolean value (True/False), corresponding to yes/no
    heatpump_living = get_valid_bool("Select (y/n): ")
    if heatpump_living is None:
        return None

    #Using global constants and dictionary to give a description and price  
    print (f"Would you like to add a {HEATPUMP_BED} heat pump in the bedroom? +${PRICES['heatpump_bedroom']:,.2f}?")
    #Uses validation function to get a boolean value (True/False), corresponding to yes/no
    heatpump_bedroom = get_valid_bool("Select (y/n): ")
    if heatpump_bedroom is None:
        return None

    print("\nSocket Upgrades - ")
    #Using dictionary to give the corresponding price  
    #Uses validation function to get an integer, corresponding to number of 1g sockets
    print(f"Ýou can add up 12 sockets total, this is including 1G +${PRICES['socket_1g']:,.2f} ea, and 2G +${PRICES['socket_2g']:,.2f} ea")
    socket_1g_count = get_valid_int(f"How many extra 1G sockets would you like?", min_val=0, max_val=12)
    if socket_1g_count is None:
        return None

    #They are allowed maximum of 12 sockets total
    #Number of 2g sockets allowed calculated from previous input of 1g sockets
    remaining_allowed = 12 - socket_1g_count
    #If they ordered less than 12 1g sockets
    if remaining_allowed > 0:
        #Prints the maximum amount they can order
        print(f"(You can add up to {remaining_allowed} extra 2G sockets)")
        #Uses the value in the range to ensure they can't add too many
        socket_2g_count = get_valid_int(f"How many extra 2G sockets would you like?", min_val=0, max_val=remaining_allowed)
        if socket_2g_count is None:
            return None
    
    #If they order 12 1g sockets, can't order any 2g therefore set to 0
    else:
        print(f"Sorry, you cannot add any 2G as you have reached the maximum number of sockets")
        socket_2g_count = 0

    print("\nNetwork Upgrades - ")
    #If the customer adds network points, they will need a switch in the build
    print(f"Ýou can add 2 - 8 sockets, or none, +${PRICES['network_point']:,.2f} ea")
    print (f"Please note, adding 2 or more network points will mean a ${PRICES['network_switch']:,.2f} switch is added automatically")
    #Loop will continue until a valid integer is entered
    while True:
        #Calls validation function to ensure input is whole number within range 
        network_points_count = get_valid_int("How many network points required?: ", min_val=0, max_val=8)
        #Because they can't add only 1 point, it must not be considered valid
        if network_points_count == 1:
            #Loop continues
            print("Try again, you cannot select only 1 network point")
        elif network_points_count is None:
            return None    
        else:
            #Returns a valid number of network points
            break
    print()

    #All the upgrade options are returned as a tuple to be used for quote
    return bathroom_option, kitchen_option, livingroom_option, heatpump_living, heatpump_bedroom, socket_1g_count, socket_2g_count, network_points_count
           
#Function for returning stored data
def view_saved_quotes(quotes_data: list):
    """Displays a summary list of all stored quote records, loaded from the JSON file

    Args:
        quotes_data (list): A list of dictionaries representing saved quotes in file.
    """
    #Checks if the list is empty, will return False, not displaying any records, ends function
    if not quotes_data:
        print("\nNo quotes found.")
        return

    print("\nSaved Quote History ")
    print("-" * 30)
    #Iterates through saved quote dictionaries, i start at 1 for better readability for user
    #Each dictionary is item
    for i, item in enumerate(quotes_data, start=1):
        #Gets customer dictionary from nested dictionary
        cust = item["customer"]
        #Print summary line featuring reference ID, customer name, and formatted total cost
        print(f"{i}. Ref: {item['ref_number']} | Name: {cust['name']} | Total: ${item['final_total']:,.2f}")

def save_formatted_quote(quote: Quote):
    """
    Creates and saves a clean text version of the quotation that the user can open and print

    Args:
        quote (Quote): The Quote object containing all customer details and selections
    """
    costs = quote.calculate_total()
    
    #Create a filename using the reference number
    filename = f"Quote_{quote.ref_number}"

    #Opens the new file in write mode so the formatted quote can be saved
    with open(filename, "w", encoding="utf-8") as f:

        #Writes the company information at the top
        f.write("-" * 65 + "\n\n")
        f.write("Waimak Build Co\n")
        f.write("Rangiora, North Canterbury\n")
        f.write("Phone: 03 1234567\n")
        f.write("Email: Office@wbc.co.nz\n\n")
        f.write("-" * 65 + "\n\n")

        #Writes customers personal input and reference number
        f.write(f"Quote Reference:  {quote.ref_number}\n")
        f.write(f"Date Generated:   {datetime.datetime.now().strftime('%d/%m/%Y')}\n\n")
        f.write("Customer Details\n")
        f.write("-" * 40 + "\n")
        f.write(f"Name:             {quote.customer.name}\n")
        f.write(f"Phone:            {quote.customer.phone}\n")
        f.write(f"Address:          {quote.customer.address}\n")
        f.write(f"Trade Account:    {'Yes (10% Discount)' if quote.customer.is_trade else 'No'}\n\n")

        #Writes the section showing all upgrades the customer selected 
        f.write("Selected Upgrades\n")
        f.write("-" * 40 + "\n")
        f.write(f"Bathroom:               Option {quote.bathroom_option}\n")
        f.write(f"Kitchen:                Option {quote.kitchen_option}\n")
        f.write(f"Living Room:            Option {quote.livingroom_option}\n")
        f.write(f"Living Room Heat Pump:  {'Yes' if quote.heatpump_living else 'No'}\n")
        f.write(f"Bedroom Heat Pump:      {'Yes' if quote.heatpump_bedroom else 'No'}\n")
        f.write(f"Extra 1G Sockets:       {quote.socket_1g_count}\n")
        f.write(f"Extra 2G Sockets:       {quote.socket_2g_count}\n")
        f.write(f"Network Points:         {quote.network_points_count}")
        #Doesn't write switch if there were no points selected 
        if quote.network_points_count > 0:
            f.write(" (+ Network Switch)\n")
        else:
            f.write("\n")
        f.write("\n")

        #Writes the cost summary section using the values calculated before
        f.write("Cost Summary\n")
        f.write("-" * 40 + "\n")
        f.write(f"Upgrades (excl. GST):   ${costs['cost_upgrades']:,.2f}\n")
        f.write(f"GST on Upgrades (15%):  ${costs['cost_gst']:,.2f}\n")
        f.write(f"Base Kit Cost:          ${BASIC_KIT:,.2f}\n")
        #Will only write the discount line if trade member
        if quote.customer.is_trade:
            f.write(f"Trade Discount (10%):   -${costs['discount_amount']:,.2f}\n")
        f.write("\n")
        f.write(f"Total (incl. GST):      ${costs['final_total']:,.2f}\n")
        f.write("-" * 65 + "\n")
        f.write("Thank you for choosing Waimak Build Co\n")

    #Confirms with the user the quote has been saved and gives them the filename
    print(f"\nThe quote saved as: {filename}, you can open this file and print it if needed ")

def main():
    """Serves as the primary function for the application interface

    Loads existing quote history from file and presents an interactive main menu 
    allowing users to create new quotes, view saved summaries, or exit cleanly
    """
    #Loads existing saved quotes from JSON file when opened
    quotes_data = load_quotes()

    #Loop will repeatedly run to present the main application menu 
    while True:
        #Prints all the available applications  
        print("-" * 50)
        print("Welcome to the Waimak Build Co, Quotation Creator!")
        print("1. Create New Quote")
        print("2. View Saved Quotes Summary")
        print("3. Exit")
        print("-" * 50)

        #Collects input on desired menu
        choice = input("Choose an option (1-3): ").strip()

        #If user chooses to create quote
        if choice == "1":

            #Runs function to collect personal details, instantiates Person object
            customer = get_user_details()

            #Lets quote end without being submitted
            if customer is None:
                print("\nQuote cancelled, returning to main menu\n")
                continue

            #Lets quote end without being submitted
            build_details = get_build_details()
            if build_details is None:
                print("\nQuote cancelled, returning to main menu\n")
                continue

            #Unpacks tuple of build options returned from get_build_details()
            (bathroom_option, 
             kitchen_option, 
             livingroom_option, 
             heatpump_living, 
             heatpump_bedroom, 
             socket_1g_count, 
             socket_2g_count, 
             network_points_count) = build_details

            #Instantiates a new Quote object using collected user inputs
            new_quote = Quote(customer, 
                              bathroom_option, 
                              kitchen_option, 
                              livingroom_option, 
                              heatpump_living, 
                              heatpump_bedroom, 
                              socket_1g_count, 
                              socket_2g_count, 
                              network_points_count)

            #Displays the financial details of Quote object
            new_quote.display_quote()
            #This converts the object to dictionary format, appends to list
            quotes_data.append(new_quote.object_to_dict())
            #The updated list is written back to JSON file to be stored
            save_quotes(quotes_data)
            #Shows the addition went successfully
            print("Quote successfully saved to file!\n")

            if get_valid_bool("Would you like a file of your quote to print? (y/n): "):
                save_formatted_quote(new_quote)



        #If the user has chosen to view saved files
        elif choice == "2":
            #Display summary list of all previously saved quotes by running function
            view_saved_quotes(quotes_data)

        #If the user has completed their tasks and wants to exit application
        elif choice == "3":
            #Prints exit message and break out of main loop to end program execution
            print("\nThank you for using Waimak Build Co Quotation Creator. Goodbye!")
            break
        #To handle invalid menu selections outside of choices 
        else:
            print("\nSorry, that isn't an option we provide")

#Ensure main() executes only when script is run directly
if __name__ == "__main__":
    main()
