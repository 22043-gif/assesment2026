#Stella Jones
#02.09.2026
#Programming Assesment 
#“Waimak Build Co ” Quotation Creator

#Libraries 

#must add file

#Constants
BASIC_KIT = 75000
TRADE_DISCOUNT_RATE = 0.1
GST = 0.15

class Person:
    def __init__(self, name, phone, address, discount):
        self.name = name
        self.phone = int(phone)
        self.address = address
        self.discount = discount

    def __str__(self):
                return '{}, {}, {}, {}'.format(self.name, self.phone, self.address, self.discount)

    
def user_details():
        """
        Finds names
        """
        print("Welcome to the Waimak Build Co, Quotation Creator!")
        name = input("Name: ")
        phone = input("Phone number: ") 
        address = input("Address: ")

        applied_for_discount = False
        while not applied_for_discount:
            trade_member = input("Are you a trade member: ")
            if trade_member.lower() == ("yes"):
                discount = True
                applied_for_discount = True
            elif trade_member.lower() == ("no"):
                discount = False
                applied_for_discount = True
        


        
def build_details():
      """"
      This function will get user input on the details of what they want in their design
      """
      bathroom_option = False
      while not bathroom_option:
        bathroom = input("Are you a trade member: ")
        if trade_member.lower() == ("yes"):
            discount = True
            applied_for_discount = True
        elif trade_member.lower() == ("no"):
            discount = False
            applied_for_discount = True




def calculations():
      """"
      This function will use input from build_details to calculate the total cost of the build
      """
      build_details()



def add_a_person():
      """"
      This function will use details from previos functions to add a new person as an object in the Person class
      """
      user_details()
      calculations()

      return Person(name, phone, address, discount)




new_quote = user_details()
