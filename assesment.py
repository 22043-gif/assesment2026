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



def user_details():
    """
    Finds names
    """

    print("Welcome to the Waimak Build Co, Quotation Creator!")
    customer_name = input("Name: ")
    customer_phone = input("Phone number: ") 
    customer_address = input("Adress: ")


    applied_for_discount = False
    while not applied_for_discount:
        trade_member = input("Are you a trade member: ")
        if trade_member.lower() == ("yes"):
            discount = True
            applied_for_discount = True
        elif trade_member.lower() == ("no"):
            discount = False
            applied_for_discount = True
        else:
            print("Sorry, please enter your trade member status again, that wasn't a valid option")




    

def new_quote():
    """
    Runs functions 
    """

#Consants


user_details()