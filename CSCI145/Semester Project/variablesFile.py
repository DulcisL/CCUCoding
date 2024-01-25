# Create the variables class
class Variables():
    '''Description: This class is to store all and overwrite the variables used for the calculator
    Attributes:

        range (int) : Contains the range the target is at
        rangeUnits (int): Contains the number linked to the units for the range
        coefficient (float): Contains the coefficient of the bullet when in the air
        caliber (int): Contains the caliber that is being shot
        weight (float): Contains the weight of the bullet used
        muzzleVelocity (int): Contains the muzzle velocity of the round
        zero (int): Contains the range the user has zeroed their weapon
        los (float): Contains the height the optic is mounted

    Behaviors:

        none
    '''
    # Attributes
    _range = int
    _rangeUnits = str
    _coefficient = float
    _caliber = int
    _muzzleVelocity = int
    _zero = int
    _los = float
    _weight = int

    # constructor
    def __init__(self, range: int, rangeUnits: str, coefficient: float, caliber: int, muzzleVelocity: int, los: float, zero: int, weight: int):
        self._range = range
        self._rangeUnits = rangeUnits
        self._coefficient = coefficient
        self._caliber = caliber
        self._muzzleVelocity = muzzleVelocity
        self._los = los
        self._zero = zero
        self._weight = weight

    # setters and getters
    def setRange(self, range: int):
        self._range = range

    def setRangeUnits(self, rangeUnits: int):
        self._rangeUnits = rangeUnits

    def setCoefficient(self, coef: float):
        self._coefficient = coef

    def setCaliber(self, caliber: int):
        self._caliber = caliber

    def setMuzVel(self, newVelocity):
        self._muzzleVelocity = newVelocity
    
    def setLOS(self, los):
        self._los = los

    def setZero(self, newZero):
        self._zero = newZero
    
    def getWeight(self, weight):
        self._weight = weight

    def getRange(self):
        return self._range

    def getRangeUnits(self):
        return self._rangeUnits

    def getCoefficient(self):
        return self._coefficient

    def getCaliber(self):
        return self._caliber
    
    def getWeight(self):
        return self._weight

    def getMuzVel(self):
        return self._muzzleVelocity

    def getLineOfSight(self):
        return self._los

    def getZero (self):
        return self._zero

    # Actions

    # String Method
    def __str__(self):
        return f'''
        Caliber is: {self._caliber}
        Range is: {self._range} {self._rangeUnits}
        Coefficient is: {self._coefficient}
        Muzzle Velocity is: {self._muzzleVelocity}
        Zero is: {self._zero}
        '''
