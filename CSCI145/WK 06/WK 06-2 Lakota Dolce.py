''' Name: Lakota Dolce
Date: 02/16/2023
Assignment: Wk06 Assignment 2
Pseudocode:(when needed)
'''

#Import the Enums Library
from enum import Enum

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

#Set up loop environment
endAll = False
while endAll == False:
    print('\n---- Welcome to the Currency Exchange ----')
    exchange = []
    #Take user input
    userInput = input('Please enter the amount of USD you wish to exchange (Enter q to quit): ')

    #check user input
    while True:
        try:
            #Check for quit statement
            if userInput.lower == 'q':
                endAll = True
                break

            #convert input into an integer
            userInput = int(userInput)
            if userInput >= 0:
                #convert USD to other currencies
                for attribute in CurrencyDenomination:
                    exchangeRate = attribute.value

                    #Store in the list
                    exchange.append('You will recieve ' + str(userInput * exchangeRate) + f' in {attribute.name}')
                break
            else:
                raise ValueError

        #Catch the exceptions
        except Exception:
            #tell the user
                print('\n Not a valid choice')

                # take users new input
                userInput = input('Please choose which currency you would like to exchange USD into (Enter q to quit): ')
                continue

    #Print the list with description to console
    for currency in exchange:
        print(currency)