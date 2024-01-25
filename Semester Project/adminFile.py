#Imports
from userFile import *

# Create the Admin class
class Admin (User):
    '''Description: This class is to have user admin access being able to change default variables in the dropCalc and Variable classes
    
    Inheritance from the User class

    Attributes:

        average556 (float): Contains the new average coefficient for the 5.56 calculation
        average300 (float): Contains the new average coefficient for the 300 WIN MAG calculation
        average308 (float): Contains the new average coefficient for the 308 calculation
        average65 (float): Contains the new average coefficient for the 65 Creedmoor calculation

    Behaviors:

        changeVarDefaults -> Allows the admin to change the coefficients for the calculator
    '''

    # Attributes
    _average556 = float
    _average300 = float
    _average308 = float
    _average65 = float

    # Constructor
    def __init__(self):
        super().__init__()
        self._average556 = .151
        self._average300 = .507
        self._average308 = .495
        self._average65 = .585

    # Setters and getters
    def setAve556(self, average):
        self._average556 = average

    def setAve300(self, average):
        self._average300 = average

    def setAve308(self, average):
        self._average308 = average

    def setAve65(self, average):
        self._average65 = average

    def getAve556(self):
        return self._average556

    def getAve300(self):
        return self._average300

    def getAve308(self):
        return self._average308

    def getAve65(self):
        return self._average65

    # Behaviors
    def changeVarDefaults(self):
        '''Description: This method is designed to change the average coeficients used in the dropCalc class
        Parameters:
            nothing
        Return:
            average556 (float): Contains the new average coefficient for the 5.56 calculation
            average300 (float): Contains the new average coefficient for the 300 WIN MAG calculation
            average308 (float): Contains the new average coefficient for the 308 calculation
            average65 (float): Contains the new average coefficient for the 65 Creedmoor calculation
        '''
        # Allow the admin to change defaults used in the variables calculator
        #Create a menu to change values
        print('Which value would you like to change?')
        while True:
            try:
                #Take user choice
                changeValue = int(input('''
                Enter 1 for 5.56 average coefficient
                Enter 2 for .300 WIN MAG average coefficient
                Enter 3 for .308 average coefficient
                Enter 4 for 6.5 Creedmoor average coefficient \n'''))
                #Check the input
                if changeValue < 0 or changeValue > 4:
                    raise ValueError
                else:
                    #Check the input and change the value
                    match changeValue:
                        case 1:
                            self.setAve556(float(input('What is the value you want to change the coefficient to? ')))
                        case 2:
                            self.setAve300(float(input('What is the value you want to change the coefficient to? ')))
                        case 3:
                            self.setAve308(float(input('What is the value you want to change the coefficient to? ')))
                        case 4:
                            self.setAve65(float(input('What is the value you want to change the coefficient to? ')))
                        case _:
                            raise ValueError
                    #break loop if all goes well
                    break
            except Exception:
                #Tell user what went wrong
                print('You entered an invalid choice')
        #Ask user if they want to use these numbers
        print('Do you want to run the program? 1 for yes and 2 for no')
        while True:
            try:
                runChoice = int(input('Enter here: '))
                if runChoice == 1:
                    aver556 = self._average556
                    aver300 = self._average300
                    aver308 = self._average308
                    aver65 = self._average65
                    #Run menu with new value
                    variables = self.menu(aver556, aver300, aver308, aver65)
                    print(self._drop)
                #Break the loop
                break
                
            except Exception:
                print('You entered an invalid choice')

    # String method
    def __str__(self):
        #Print any changes made to the averages, and print the calculator output
        return  f'''New average coefficients are: {self._average556}, {self._average300}, {self._average308}, {self._average65}
        {self.menu()}
        '''