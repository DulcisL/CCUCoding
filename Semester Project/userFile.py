#Imports
from calculator import *
import pickle

# Create the User class
class User ():
    '''Description: This class is to create the user class for standard use
    Attributes:

    priviledges (int): Contain an integer to see the privileges of the user
    drop (float): contain the drop that is given from the calculator function in the dropCalc class


    Behaviors:

    menu -> Display the menu for the user
    runCalc -> Get the variables and create an instance of the dropCalc class
    '''
    # Attributes
    _privileges = int
    _drop = float

    # Constructor
    def __init__(self, privileges = 1):
        self._privileges = privileges
        self._drop = 0
        self._maxDis = 0

    # setters and Getters
    def setPrivileges(self, newPrivileges):
        self._privileges = newPrivileges

    def setDrop(self, drop):
        self._drop = drop

    def getPrivileges(self):
        return self._privileges

    def getDrop(self):
        return self._drop

    # Actions
    # Create the menu
    def menu(self, aver556 = .151, aver300 = .507, aver308 = .495, aver65 = .585):
        '''Description: This method is designed to get the users choice on the calculations they want to do
                Parameters:
                    choice (int): contains the choice the user made from the menu
                    variables (dict) : Containing the data needed for the calculations
                    aver... (float): Contains the average coefficients for the calibers
                Return:
                    drop (float): Contains the drop calculated from the variables
        '''

        # Set up loop environment
        stop = False
        while stop == False:
            while True:
                try:
                    # print the menu
                    print(''' \n
                    |||Welcome to the Ballistics Calculator||| 
                    Please choose an option from below 
                    Choose 1 to calculate the ballistics for 5.56 x 45 
                    Choose 2 to calculate the ballistics for 300 WIN MAG 
                    Choose 3 to calculate the ballistics for 7.62 x 51 or .308
                    Choose 4 to calculate the ballistics for 6.5 Creedmoor 
                    Enter 9 to quit \n
                    ''')
                    #take the users choice
                    choice = int(input('Enter choice 1-4 or 9 here: '))
                    if (choice > 0 and choice < 5) or choice == 9:
                        if choice == 9:
                            #terminate the program
                            print('Goodbye')
                            quit()

                        if choice == 1:
                            print(f'Choice was {choice}')
                            caliber = 556
                            # Get shooting variables
                            return self.runCalc(caliber, aver556)

                        if choice == 2:
                            print(f'Choice was {choice}')
                            caliber = 300
                            # Run method
                            return self.runCalc(caliber, aver300)

                        if choice == 3:
                            print(f'Choice was {choice}')
                            caliber = 308
                            # Run method
                            return self.runCalc(caliber, aver308)

                        if choice == 4:
                            print(f'Choice was {choice}')
                            caliber = 65
                            # Run method
                            return self.runCalc(caliber, aver65)
                            
                    else:
                        raise ValueError
                except ValueError:
                    print('Not a valid choice, try again \n ')

    # Get variables
    def getVariables(self, caliber, aver556 = .151, aver300 = .507, aver308 = .495, aver65 = .585):
        '''Description: This method is designed to get and check and store the variables needed to calculate the ballistics
            Parameters:
                caliber (int): contains the caliber the user is calculating
                aver... (float): contains the average coefficient for the specified caliber
            Return:
                rangeUnits (int) : Tells the system what units will be used for measuring range
                range (int) : Contains the distance the user inputs
                windDir (int) : Contains an integer telling the direction the wind is travelling
                windUnit (int): Tells the system what units will be used for measuring the wind speed
                windSpeed (int) : Contains the integer for the wind speed
                coefficientTrue (int): Prepares the system for the coefficient value
                coefficient (float): Takes the coefficient of the bullet for calculations
                caliber
                aver...
        '''
        #Get variables
        rangeUnits = ''
        while True:
            try:
                rangeUnits = int(input('''
                Enter the units you want to use for range 
                1 for feet
                2 for yards
                3 for meters
                4 for kilometers \n
                '''))
                if rangeUnits > 0 and rangeUnits < 5:
                    #Correct units
                    match rangeUnits:
                        case 1:
                            rangeUnits = 'ft'
                        case 2:
                            rangeUnits = 'yds'
                        case 3:
                            rangeUnits = 'm'
                        case 4:
                            rangeUnits = 'km'
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Not a valid choice try again')

        coefficientTrue = ''
        coefficient = 0
        while True:
            coefficientTrue = input('''Do you know you ballistic coefficient?
            please enter 1 for yes and 3 for no: \n''')
            try:
                coefficientTrue = int(coefficientTrue)
                if coefficientTrue == 1 or coefficientTrue == 3:
                    break
                else:
                    raise ValueError
            except ValueError:
                print('Incorrect choice try again')

        # if coefficient not known, use average coefficient
        if coefficientTrue == 3:
            if caliber == 1:
                coefficient = aver556
            if caliber == 2:
                coefficient = aver300
            if caliber == 3:
                coefficient = aver308
            if caliber == 4:
                coefficient = aver65

        # if yes use user coefficient
        if coefficientTrue == 1:
            while True:
                try:
                    coefficient = float(input('Enter the coefficient here (Enter a positive number): \n'))
                    if coefficient > 0:
                        break
                except ValueError:
                    print('Not a valid coefficient, try again')

        #Get the muzzle velocity
        muzzleVelocity = ''
        while True: 
            try:
                muzzleVelocity = int(input('Enter the muzzle Velocity to the closest integer in fps (Enter a whole number): '))
                if muzzleVelocity <= 0:
                    raise ValueError
                break
            except Exception:
                print("You entered an unusable input")
        
        los = ''
        while True:
            try:
                los = float(input("Please enter your height over bore in inches (Enter a positive number): "))
                if los <= 0:
                    raise ValueError
                break
            except Exception:
                print("You entered an invalid input")
        
        zero = 0
        while True:
            try:
                zero = int(input('Enter your zero in the same units as your range (Enter a whole number): '))
                if zero <= 0:
                    raise ValueError
                break
            except Exception:
                print("You entered an invalid input")
        
        weight = 0
        while True:
            try:
                weight = int(input('Enter the weight of the bullet in grains (to the nearest whole number): '))
                if weight <= 0:
                    raise ValueError
                break
            except Exception:
                print('You entered an invalid number')
        
        variables = [coefficient, muzzleVelocity, los, zero, rangeUnits, weight]
        return variables
            


    def runCalc(self, caliber, aver556 = .151, aver300 = .507, aver308 = .495, aver65 = .585):
        '''Description: This method is designed to get and check and store the variables needed to calculate the ballistics, then create an instance of the dropCalc Class
            Parameters:
                caliber (int): contains the caliber the user is using
                aver... (float): contains the average coefficient for the specified caliber
            Return:
                self._drop (float): contains the calculated drop
        '''
        
        #Get user range and check input
        userRange = 0
        # Check the range for correct input
        while True:
            try:
                userRange = int(input('Enter the range you wish to shoot (round to the nearest unit): '))
                if userRange > 0:
                    break
                else:
                    raise ValueError
            except Exception:
                print('Not a valid input, try again')
        
        #Call variables function
        variables = list(self.getVariables(caliber, aver556, aver300, aver308, aver65))
        #Set the variables from the function
        coefficient = variables[0]
        muzzleVelocity = variables[1]
        los = variables[2]
        zero = variables[3]
        rangeUnits = variables[4]
        weight = variables[5]
        
        # create the calculator instance
        self._drop = DropCalc(userRange, rangeUnits, coefficient, caliber, muzzleVelocity, los, zero, weight)
        #return the result
        return self._drop

    def rangeCard(self):
        '''Description: This method is designed to get and check and store the variables needed to calculate the ballistics, then create and print a file for a range card
            Parameters:
                none
            Return:
                nothing
        '''
        #Ask user if they want the old card or create a new one
        while True:
            try:
                history = input("Do you want to print the old card? (y for yes and n for no): ")
                if history.lower() == 'n':
                #Get variables
                #get increments
                    increments = 0
                    while True:
                        try:
                            increments = int(input("What increments of range do you want the card to be in(Enter a whole number)? "))
                            break
                        except Exception:
                            print("You entered an unusable input, please try again")

                    #Get max distance
                    maxRange = 0
                    while True:
                        try:
                            maxRange = int(input("What is the max range you want to go to (Enter a whole number)? "))
                            if maxRange < increments:
                                print('You cannot have a range less than the increment')
                                raise ValueError
                            break
                        except Exception:
                            print("You entered an unusable input, please try again")

                    #Get Caliber
                    caliber = 0
                    while True:
                        try:
                            # print the menu
                            print(''' \n
                            What caliber are you using? 
                            Choose 1 to calculate the ballistics for 5.56 x 45 
                            Choose 2 to calculate the ballistics for 300 WIN MAG 
                            Choose 3 to calculate the ballistics for 7.62 x 51 or .308
                            Choose 4 to calculate the ballistics for 6.5 Creedmoore 
    
                            ''')
                            #take the users choice
                            choice = int(input('Enter choice 1-4: '))
                            if choice > 0 and choice < 5:

                                if choice == 1:
                                    print(f'Choice was {choice}')
                                    caliber = 556
                                    break

                                if choice == 2:
                                    print(f'Choice was {choice}')
                                    caliber = 300
                                    break

                                if choice == 3:
                                    print(f'Choice was {choice}')
                                    caliber = 308
                                    break

                                if choice == 4:
                                    print(f'Choice was {choice}')
                                    caliber = 65
                                    break

                            else:
                                raise ValueError
                        except ValueError:
                            print('Not a valid choice, try again \n ')

                    #Call variables function
                    variables = self.getVariables(caliber)

                    coefficient = variables[0]
                    muzzleVelocity = variables[1]
                    los = variables[2]
                    zero = variables[3]
                    rangeUnits = variables[4]
                    weight = variables[5]

                    userRange = increments
                    while True:
                        try:
                            #create the file
                            rangeCard = open('RangeCard.txt', 'w+')

                            drop  = 0
                            #create the card
                            while userRange <= maxRange:
                                #Calculate the drop at each increment
                                drop = DropCalc(userRange, rangeUnits, coefficient, caliber, muzzleVelocity, los, zero, weight)
                                #Write it to the file
                                rangeCard.write(f'At {userRange} {rangeUnits} there is {drop.calculate()} inches of drop \n')

                                #increase the range for the drop
                                userRange += increments
                            #Close the range card
                            rangeCard.close()

                            #del range card
                            del rangeCard

                            #Read from the card
                            rangeCard = open('RangeCard.txt', 'r')
                            #Call read method
                            content = rangeCard.readlines()
                            #Itereate through the file
                            for line in content:
                                #Print each line
                                print(line)


                            #Create backup file
                            with open('backup.txt', 'wb') as backup:
                                # Create backup of object
                                pickle.dump(drop, backup)
                            #Close the backup
                            backup.close()

                            #Print the backup
                            #Open the backup in read
                            backup = open('backup.txt', 'rb')
                            # Print the back-up
                            backupObject = pickle.load(backup)
                            print(backupObject)
                            backup.close()

                            #break the loop while loop if all went well
                            break
                        except Exception:
                            #Create the file
                            #open('RangeCard.txt', 'wb')
                            print('File doesnt exist')

                        finally:
                            #close the range card
                            rangeCard.close()
                    #Break the loop
                    break
                #If they want to print the card
                if history.lower() == 'y':
                    try:
                        #Read from the card
                        rangeCard = open('RangeCard.txt', 'r')
                        #call the read method
                        content = rangeCard.readlines()
                        #Iterate through the list
                        for line in content:
                            #print the content
                            print(line)
                        #close the card
                        rangeCard.close()

                        #Print the backup
                        #Open the backup in read
                        backup = open('backup.txt', 'rb')
                        # Print the back-up
                        backupObject = pickle.load(backup)
                        print(backupObject)
                        backup.close()

                    #catch the exceptions
                    except Exception:
                        #tell the user what went wrong
                        print('Range card does not exist yet, please create a new one')
                    return
                else:
                    raise ValueError
            except Exception:
                print('You entered an invalid input')
                return

    def __str__(self):
        #Return all variables and the output of the calculator
        return f'{self.menu()}'
