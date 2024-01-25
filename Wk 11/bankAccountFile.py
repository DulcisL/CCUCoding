class Bank ():
    '''Description: This class is to store all and overwrite the variables used for the calculator
    Attributes:

        _total (float): Contain the total for the account

    Behaviors:
        SETotal (newTotal): set the total for the class
        getTotal(): Get the total for the class
        __float__(): Override the float method 
    '''
    #Attribute
    _total = float

    #Constructor
    def __init__ (self, total: float = 0):
        self._total = round(total, 2)
    
    #setters and getters
    def setTotal (self, newTotal):
        self._total = newTotal

    def getTotal(self):
        return round(self._total, 2)

    #Override float
    def __float__(self):
        return round(self._total, 2)