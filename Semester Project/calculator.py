#Imports
from variablesFile import *
from math import *

# Create the calculator
class DropCalc (Variables):
    '''Description: This class is to Calculate and return the values for the drop as well as convert units of measurement
    
    Inheritance from the Variables class
    
    Attributes:

        variables (obj): Contains the variables instance
        drop (float): Contains the drop of after calculating it

    Behaviors:

        convertMeters -> Convert the distance to meters
        convertMuzzle -> Convert the muzzle velocity to m/s
        calculate -> Calculate the drop using the variables

    '''
    # Attributes
    _variables = object
    _drop = float

    #Constructor
    def __init__(self, range, rangeUnits, coefficient, caliber, muzzleVelocity,  los, zero, weight):
        super().__init__(range, rangeUnits, coefficient, caliber, muzzleVelocity,  los, zero, weight)
        self._drop = 0

    # setters / getters
    def setDrop(self, drop):
        self._drop = drop

    def getDrop(self):
        return self._drop

    
    # Actions
    # Convert range units to m
    def convertMeters(self):
        '''Description: This method is designed to convert the units to meters for the distance
        Parameters:
            curDistance (int): Contains the distance given by the user
            curUnits (str): Contains the units the user gave
            newDistance (float): Contains the new distance
        Return:
            newDistance (float): Contains the new distance
        '''
        curUnits = self.getRangeUnits()
        curDistance = self.getRange()
        #Convert from current units to Meters
        if curUnits == 'ft':
            newDistance = curDistance / 3.281
            return newDistance
        if curUnits == 'yds':
            newDistance = curDistance / 1.094
            return newDistance
        if curUnits == 'm':
            return curDistance
        if curUnits == 'km':
            newDistance = curDistance * 1000
            # change the variables to the new unit
            return newDistance
        
        return self._range
    
    #convert los to meters
    def convertLOS(self):
        '''Description: This method is designed to convert the units to meters
        Parameters:
            none
        Return:
            los (float): Contains the line of sight converted to meters
        '''
        #Get line of sight
        los = self.getLineOfSight()
        #convert and return
        los = los / 39.37
        return los
    
    def convertZero(self):
        '''Description: This method is designed to convert the units to meters
        Parameters:
            none
        Return:
            newZero (float): Contains the zero distance converted to meters
        '''
        curUnits = self.getRangeUnits()
        curZero = self.getZero()
        # Convert from current units to Meters
        if curUnits == 'ft':
            newZero = curZero / 3.281
            return newZero
        if curUnits == 'yds':
            newZero = curZero / 1.094
            return newZero
        if curUnits == 'm':
            return curZero
        if curUnits == 'km':
            newZero = curZero * 1000
            # change the variables to the new unit
            return newZero


    # calculate the drop
    def calculate(self):
        '''Description: This method is designed to calculate the drop in inches
        Parameters:
            none
        Return:
            drop (str): Contain the calculated drop  in inches
        '''
        try:
            #Set variables and set to needed units

            #Set the zero
            zero = self.convertZero()
            #Set range
            r = self.convertMeters()
            #Ser Coefficient
            c = self.getCoefficient()
            #Set initial velocity
            Vo = self.getMuzVel()
            #Set line of sight
            los = self.convertLOS()
            #Set gravity
            g = 9.8
            #Set air pressure
            p = 1.2
            #Set mass / (convert to kg)
            m = self.getWeight() / 15430
            #set bullet area
            Ab = 4.8 * 10**-5

            #Calculate the adjacent (hypotenuse)
            H = sqrt(zero**2 - los**2)

            #Calculate Velocity in x and y direction
            Vx = Vo * cos(zero/H)
            Vy = Vo * sin(los/H)

            #Calculate time of flight
            t = sqrt(r / Vx)

            drop = round(((((Vy * t) - ((1/2) * g * t**2)) - ((c * p * Ab * Vy**2 * t**2) / 2)))* 39.37, 1)
            self._drop = drop
            return drop
        except Exception:
            print('Number could not be calculated with those variables, please try again')
    # string method
    def __str__(self):
        return f'''Variables are: {super().__str__()}
        Drop is {self.calculate()} inches
        '''