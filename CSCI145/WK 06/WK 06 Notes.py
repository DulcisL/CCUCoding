#what is an enum
#an enumeration is a set of members associated with unique constant values.
#Python provides you with the enum module that contains the Enum type for defining new enumerations.
#You define a new enumeration type by subclassing the Enum class.

#an object is a collection of data with associated behaviors.
#How do we differentiate between types of objects?

#Apples and oranges are both objects, but it is a common adage that they cannot be compared. Apples and oranges aren't
#modeled very often in computer programming

#brain storm the differences

#you must install the Enum Package
#Import from the enum library
from enum import Enum
import random

#creating an enum

#class comments
#class Header (Doc Strings)
'''Description: This class is to model a traffic light to change the color status
Attributes:
RED (int) : color of the traffic light
YELLOW (int) :color of the traffic light
GREEN (int) :color of the traffic light
Behaviors:
nothing
'''
#create a traffic light
class TrafficLight(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3

#test Enum
#create an instance of the class
#create a copy of this class into a variable
light1Status = TrafficLight.RED
print(light1Status)
light1Status = TrafficLight.YELLOW
light2Status = TrafficLight.GREEN
print(light1Status)
print(f'Traffic light 2 is {light2Status}')
#check if an instance contains an enum attribute
if light1Status == TrafficLight.RED:
    print("Stop!!! Light is red")
#print the value of the RED attribute
print(TrafficLight['RED'])
print(TrafficLight(1))

#create an num for car controls
class CarControls(Enum):
    FORWARD = 1
    BACKWARDS = -2
    LEFT = 3
    RIGHT = 4
    UTURN = 5
    STOP = 6
    DIAG = 7

#Function to control the car
def moveCar (userChoice, distance):
    # to create a random number randint function takes 2 integers
    # The first is the start range
    # The second is the end range
    trafficLightStatus = random.randint(TrafficLight(1).value, TrafficLight(len(TrafficLight)).value)
    # traffic light
    # user a random number to choose an item from the trafficlight enum

    if trafficLightStatus == TrafficLight.RED:
        print(f'Car stopped at RED light, car travelled {distance} miles')
        print('Choose another direction: ')

    if trafficLightStatus == TrafficLight.YELLOW:
        distance += TrafficLight(userChoice).value
        print(f'Car speeds through the light, car travelled {distance} miles')
        print('Choose another direction: ')

    if trafficLightStatus == TrafficLight.GREEN:
        distance += TrafficLight(userChoice).value
        print(f'Car goes through the light, car travelled {distance} miles')
        print('Choose another direction: ')

#scenario
#create a driving simulator
#use a menu for the users to move the car
#loop through the enum to make a list for the user to choose
userDirection = 0
distance = 0
print('Welcome to the drive simulator')
print('Enter a number besides the control to move the car')
for attribute in CarControls:
    print(f"{attribute.value} - Move car {attribute.name}")
def askUser (count):
    try:
        if count > 5:
            return count
        userDirection = input('Enter a number from the control here: ')
        userDirection = int(userDirection)
        moveCar(userDirection, 3)
        return askUser(count + 1)
    except ValueError:
        print('You must enter a number')


askUser(0)

#create an enum with the car controls
#use the enum TrafficLight to simulate the lights at an intersection
#simulating the drive
    #Allow, the user to select a direction for the car to move
    #make at least 3 intersections to use the TrafficLight
intersection1 = TrafficLight.RED
intersection2 = TrafficLight.YELLOW
intersection3 = TrafficLight.GREEN

myEnumList = []
myEnumList.append(intersection3)
    #The user will choose directions from a menu one at a time, and your program will react
#simulate keep car distance
#hit at least one traffic light
#respond to the color of the light
#allow the user to choose another direction

    #Once the user chooses 5 directions, the program will end.
#store the directions in a list
#store the traffic light states in a list

#print the status of the lights from the drive
#print the directions for the car from the drive
