#Imports
from variablesFile import *
from math import *

CALIBER_DIAMETERS_IN = {
    556: 0.224,
    300: 0.308,
    308: 0.308,
    65: 0.264
}
DEFAULT_DIAMETER_IN = 0.308
INCH_TO_METER = 0.0254

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

    def getBulletArea(self):
        diameter_in = CALIBER_DIAMETERS_IN.get(self.getCaliber(), DEFAULT_DIAMETER_IN)
        diameter_m = diameter_in * INCH_TO_METER
        radius_m = diameter_m / 2
        return pi * radius_m ** 2
    
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
            #Set Coefficient
            c = self.getCoefficient()
            #Set initial velocity
            Vo_fps = self.getMuzVel()
            #convert to m/s
            Vo = Vo_fps * 0.3048
            #Set line of sight
            los = self.convertLOS()
            #Set gravity
            g = 9.8
            #Set air pressure
            p = 1.2
            #Set mass / (convert to kg)
            m = self.getWeight() * 0.00006479891

            #Calculate the adjacent (hypotenuse)
            H = sqrt(zero**2 + los**2)
            theta = asin(los / H) if H > 0 else 0
            #Calculate Velocity in x and y direction
            Vx = Vo * cos(theta)
            Vy = Vo * sin(theta)

            #Calculate time of flight
            t = r / Vx

            bullet_area = self.getBulletArea()
            if bullet_area <= 0:
                raise ValueError
            speed = sqrt(Vx**2 + Vy**2)
            if speed <= 0:
                return 0.0
            drag_coeff = max(c, 0.001)
            drag_force = 0.5 * p * drag_coeff * bullet_area * speed**2
            drag_accel = drag_force / m
            vertical_drag = drag_accel * (Vy / speed)
            drop_m = (Vy * t) - (0.5 * (g + vertical_drag) * t**2)

            drop = round(drop_m * 39.37, 1)
            self._drop = drop
            return drop
        except Exception:
            print('Number could not be calculated with those variables, please try again')
    # string method
    def __str__(self):
        return f'''Variables are: {super().__str__()}
        Drop is {self.calculate()} inches
        '''
