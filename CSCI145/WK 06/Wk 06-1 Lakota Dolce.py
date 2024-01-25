''' Name: Lakota Dolce
Date: 02/16/2023
Assignment: Wk06 Assignment 1
Pseudocode:(when needed)
'''
#Import the Enums Library
from enum import Enum

'''Description: This class is to model the different sizes for clothes
Attributes:
    SMALL (int): Contain the value for the specific size
    MEDIUM (int): Contain the value for the specific size
    LARGE (int): Contain the value for the specific size
    XLARGE (int): Contain the value for the specific size
Behaviors:
nothing
'''
class Sizes (Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    XLARGE = 4

'''Description: This class is to model an expanded list of errors
Attributes:
    WRONGINPUT (int): Contain the returned value for an expanded list of errors
    OUTOFSTOCK (int): Contain the returned value for an expanded list of errors
    ORDERTOSMALL (int): Contain the returned value for an expanded list of errors
    ORDERTOBIG  (int): Contain the returned value for an expanded list of errors
Behaviors:
nothing
'''
class ErrorMessages (Enum):
    WRONGINPUT = 1
    OUTOFSTOCK = 2
    ORDERTOSMALL = 3
    ORDERTOBIG = 4

'''Description: This class is to model currency exchange rates for common currencies
Attributes:
    GBP (int): contain the exchange rate for the currency into USD
    EURO (int): contain the exchange rate for the currency into USD
    YEN (int): contain the exchange rate for the currency into USD
    ASD (int): contain the exchange rate for the currency into USD
Behaviors:
nothing
'''
class CurrencyDenomination (Enum):
    GBP = .83
    EURO = .94
    YEN = 133.86
    ASD = 1.45

'''Description: This class is to model a conversion rate for speeds
Attributes:
    MPH (int): contain the baseline 
    KMH (int): contain the conversion rate from MPH
    FPS (int): contain the conversion rate from MPH
    MPS (int): contain the conversion rate from MPH
Behaviors:
nothing
'''
class Speeds (Enum):
    MPH = 1
    KMH = 1.61
    FPS = .45
    MPS = 1.47

'''Description: This class is to model what floor you are on in a building
Attributes:
    FIRSTFLOOR (int): Reports what floor an elevator is on
    SECONDFLOOR (int): Reports what floor an elevator is on
    THIRDFLOOR (int): Reports what floor an elevator is on
    FOURTHFLOOR (int): Reports what floor an elevator is on
Behaviors:
nothing
'''
class Levels (Enum):
    FIRSTFLOOR = 1
    SECONDFLOOR = 2
    THIRDFLOOR = 3
    FOURTHFLOOR = 4

'''Description: This class is to model the days of the week
Attributes:
    MONDAY (int): contains the name and value of the day of the week
    TUESDAY (int): contains the name and value of the day of the week
    WEDNESDAY (int): contains the name and value of the day of the week
    THURSDAY (int): contains the name and value of the day of the week
    FRIDAY (int): contains the name and value of the day of the week
Behaviors:
nothing
'''
class DaysOfWeek (Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5

'''Description: This class is to model the months and a value to it
Attributes:
    JANUARY (int): Contains the number related to the month of the year
    FEBRUARY (int): Contains the number related to the month of the year
    MARCH (int): Contains the number related to the month of the year
    APRIL (int): Contains the number related to the month of the year
Behaviors:
nothing
'''
class Months (Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4

'''Description: This class is to model the year an order was placed
Attributes:
    TWENTY (int): contains the year the order was placed
    TWENTYONE (int): contains the year the order was placed
    TWENTYTWO (int): contains the year the order was placed
    TWENTYTHREE (int): contains the year the order was placed

Behaviors:
nothing
'''
class Years (Enum):
    TWENTY = 2020
    TWENTYONE = 2021
    TWENTYTWO = 2022
    TWENTYTHREE = 2023

#Creating the instance for the Sizes Enum
for attribute in Sizes:
    #print the values and names to the console
    print(f'Please put in {attribute.value} for size {attribute.name}')

# Creating the instance for the ErrorMessages Enum
print('\n')
for attribute in ErrorMessages:
    # print the values and names to the console
    print(f'The errors are {attribute.name} and will return {attribute.value}')

#Creating the instance for the CurrencyDenomination Enum
print('\n')
for attribute in CurrencyDenomination:
    # print the values and names to the console
    print(f'The currency is {attribute.name} and it can be exchanged at a rate of {attribute.value}')

#Creating the instance for the Speeds Enum
print('\n')
for attribute in Speeds:
    # print the values and names to the console
    print(f'The speed is {attribute.name} and it can be converted by multiplying by {attribute.value}')

#Creating the instance for the Levels Enum
print('\n')
for attribute in Levels:
    # print the values and names to the console
    print(f'You are on the {attribute.name} or floor {attribute.value}')

#Creating the instance for the DaysOfWeek Enum
print('\n')
for attribute in DaysOfWeek:
    # print the values and names to the console
    print(f'Day {attribute.value} of the week is {attribute.name}')

#Creating the instance for the Months Enum
print('\n')
for attribute in Months:
    # print the values and names to the console
    print(f'The {attribute.value} is {attribute.name}')

# Creating the instance for the Years Enum
print('\n')
for attribute in Years:
    # print the values and names to the console
    print(f'Your choice is {attribute.value} for {attribute.name}')
