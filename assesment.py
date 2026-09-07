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
'''
def build_details():
      """"
      This function will get user input on the details of what they want in their design
      """

def calculations():
      """"
      This function will use input from build_details to calculate the total cost of the build
      """
      build_details()

'''

user_details()