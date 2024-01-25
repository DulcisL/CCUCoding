''' Name: Lakota Dolce
Date: 4/02/2023
Assignment: Wk 12 Assignment 1
Pseudocode:(when needed)
'''
#Imports
import random
import SearchesFile as searches

#Create the class
class GuessingGame():
    '''Description: This class is to create a random list of numbers between 0, 2000 and let the user attempt to guess
    a number from the list

    Attributes:
    gameList (list): Contains the list of numbers to guess from
    lenList (int): contains the length the user wants the list to be
    choice (int): Contains the number the user is guessing 
    low (int): Contains the next lower number from the user
    high (int): Contains the next higher number from the user
    
    Behaviors:
    findNumber() -> Looks for the number in the random list
    nextNumber(choice) -> Looks for the next highest and/or lowest number in the list if the users choice wasn't found

    '''
    #Attributes
    _gameList = list
    _lenList = int
    _choice = int
    _low = int
    _high = int

    #Constructor
    def __init__ (self, choice, listLen):
        self._choice = choice
        self._gameList = random.sample(range(0, 2000), listLen)
        self._lenList = listLen
        self._low = choice
        self._high = choice

    
    #Behaviors
    #Find the number
    def findNumber (self):
        '''Description: This method is designed to check for the guessers input and search for it through a list
        Parameters:
            none

        Return:
            1 for a pass
            -1 for a fail
        '''

        list = self._gameList
        length = self._lenList
        choice = self._choice
        
        #call and check the search function
        search = searches.Search()
        index = search.linearSearch(list, length, choice)
        if index != -1:
            #If found print the congrats
            print('Congrats, your number was found')
            return 1
        #if it didn't find the number
        else:
            self.nextNumber(choice)
        return -1
    
    def nextNumber(self, choice):
        '''Description: This method is designed to find the closest number in the list to the users choice
        Parameters:
            choice (int): contains the users choice

        Return:
            1 for a pass
            -1 for a fail
        '''
        list = self._gameList
        low = self._low
        high = self._high
        search = searches.Search()
        lowNum = -1
        highNum = -1

        #Get Low number
        while lowNum == -1:
            if low > 0:
                low -= 1
                lowNum = search.linearSearch(list, length, low)
            else:
                lowNum = -50000
                break
        
        #Get High number
        while highNum == -1:
            if high < 2000:
                high += 1
                highNum = search.linearSearch(list, length, high)
                
            else:
                highNum = 50000
                break
        #check and print the result
        if lowNum != -1 and highNum != -1:
            if (choice - lowNum) < (highNum - choice):
                print(f"Your number wasn't found but {low} was")
                return 1
            if (choice - lowNum) > (highNum - choice):
                print(f"Your number wasn't found but {high} was")
                return 1
        else:
            return -1

    def __str__ (self):
        return f"The number to seach was {self._choice}\nThe length of the list was {self._lenList}\nThe list was \n{self._gameList}"

#Get and test user input
while True:
    print('Welcome to the guessing game')
    try:
        length = int(input('How many numbers do you want to guess from: '))
        choice = int(input('Please enter a random integer between 0 and 2000: '))
        if choice >= 2000 or choice <= 0:
            raise ValueError
        #create the instance of the class
        game = GuessingGame(choice, length)
        #call the game method
        game.findNumber()
    except Exception:
        #tell the user what went wrong
        print("You entered a number outside of the range, please try again")