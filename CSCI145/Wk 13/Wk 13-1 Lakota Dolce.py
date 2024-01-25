''' Name: Lakota Dolce
Date: 4/15/2023
Assignment: Wk 13 Assignment 1
Pseudocode:(when needed)
'''
# Imports
from LinkedListServices import *
from random import *

#Create driving simulator
class Drive():
    '''Description: This class is to create a text base driving simulator

        Attributes:
        light (int): Contains what status the light is in (0: Red, 1: Yellow, 2: Green)
        right, left, forward, and reverse (int): determine the available directions (0 not available, 1 available)
        distance (int): Contains the distance travelled
        last(int): the last distance travelled

        Behaviors:
        driving (): Runs the simulation for the game
        redLight(): Prints the users results and resets the game for another round
        '''

    #Attributes
    _light = int
    _right = int
    _left = int
    _forward = int
    _reverse = int
    _distance = int
    _last = int

    #Constructor
    def __init__(self):
        self._light = 2
        self._right = 1
        self._left = 1
        self._forward = 1
        self._reverse = 0
        self._distance = 0
        self._last = 0
    
    #behaviors
    def driving(self):
        '''Description: This method is designed to run the simulator, take and check  all user input and call other methods as needed
        Parameters:
            none

        Return:
            none
        '''

        #Get situation
        light = self._light
        right = self._right
        left = self._left
        forward = self._forward
        reverse = self._reverse

        #Check what the light, 0: Red, 1: Yellow, 2: Green
        if light < 3 and light > 0:
            #Print the choices

            if left == 1:
                print('Enter 1 to go Left')
            if forward == 1:
                print('Enter 2 to go Forward')
            if right == 1:
                print('Enter 3 to go Right')
            if reverse == 1:
                print('Enter 4 to go Backwards (doing so will take away distance and that direction)')

            if left != 1 and forward != 1 and right != 1 and reverse != 1:
                print(f"You have hit a dead end, you made it {self._distance} meters ")
                self.redLight()

            #set up environment
            direction = 0
            #Get user input
            while direction <= 4:
                try:
                    #Get direction and check it
                    direction = int(input("Which direction would you like to go? (enter any number over 4 to quit) "))
                    if direction > 4 or direction < 1:
                        raise ValueError
                    
                    if direction != 4:
                        #keep last distance change
                        lastDistance = randrange(100, 1000, 1)
                        self._distance += lastDistance
                        self._last = lastDistance
                        print(f"You have travelled {self._distance} meters")
                        #Keep track of directions
                        node.addNode(direction)
                        #Add to the count
                        self.createNew()
                        self.driving()

                    if direction == 4:
                        #If they went back delete the last node if possible
                        if self._distance > 0:
                            node.deleteHeadNode()
                            self._distance -= self._last
                            print(f"You have travelled {self._distance} meters")
                            self.createNew()
                        
                        #Check if the distance is at or below zero
                        if self._distance <= 0:
                            self._distance = 0
                            print("You can't go back anymore")
                            self._left = 1
                            self._right = 1
                            self._forward = 1
                            self. _reverse = 0
                        self.driving()
                #If user wants to quit set light to zero and quit the program
                except Exception:
                    light = 0
                    break

        if light == 0:
            #Tell user how far they went
            print(f"You hit a red light! \nYou made it {self._distance} meters from the start")
            self.redLight()
            #Tell user the directions they went
            
    def redLight(self):
        '''Description: This method is designed to reset the instance, and linked list
        Parameters:
            none

        Return:
            -1 for a fail
        '''

        #Create list for directions
        directions = []
        #Iterate through the nodes and store data
        directions = node.iterate(directions)
        #Check the directions
        for i in reversed(directions):
            match i:
                case 1:
                    #Print the directions
                    print('You travelled left')
                case 2:
                    print('You travelled forward')
                case 3:
                    print('You travelled right')

        while True:
            try:
                #Ask the user to try again
                again = input("Would you like to try again? (y for Yes and n for No): ")
                #Check input
                if again.lower() == 'y':
                    #Reset and run again
                    #Reset the node
                    try:
                        while node:
                            node.deleteHeadNode()
                    except Exception:
                        pass
                    #Reset the simulator
                    self.__init__()
                    #Start again
                    self.driving()
                #If no then end the program
                elif again.lower() == 'n':
                    print('Goodbye')
                    quit()
                else:
                    raise ValueError
            except Exception:
                print("You entered an invalid input, please try again")

            return -1
            

    def createNew(self):
        '''Description: This method is designed to create a new instance of the traffic light for the user
        Parameters:
            none

        Return:
            none
        '''

        #Change the environment
        self._right = randrange(0,2,1)
        self._left = randrange(0,2,1)
        self._forward = randrange(0,2,1)
        self._reverse = 1
        self._light = randrange(0,2, 1)

#Start
print("-----Welcome to the driving simulator-----")
drive = Drive()
node = LinkedList()
drive.driving()