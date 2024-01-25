''' Name: Lakota Dolce
Date: 2/22/2023
Assignment: Wk 07 Assignment 2
Pseudocode:(when needed)
'''
#import needed library
from datetime import datetime
#Create the class
class Car():
        '''Description: This class is to model a car and to compute the age, sales and state tax
         and the cars depreciation
        Attributes:
            Name (str): Contain the cars name
            Make (str): Contain the brand of the car
            Model (str): Contain the model of the car
            Year (int): Contain the year the car was manufactured
            price (int): contain the price of the car
        Behaviors:
            addRaise() -> Change the users salary with a 5% increase
            lengthOfEmployment -> Calculate the length the person has been employed
            evalCheck -> Check if the person needs to be evaluated
        '''
        #set attributes
        _Name = ''
        _Make = ''
        _Model = ''
        _Year = 0
        _price = 0
        #create initializer
        def __init__(self):
            self.Name = ''
            self.Make = ''
            self.Model = ''
            self.Year = 0
            self.price = 0
        #create setters
        def setName(self, newName):
            self._Name = newName
        def setMake(self, newMake):
            self._Make = newMake
        def setModel(self, newModel):
            self._Model = newModel
        def setYear(self,newYear):
            self._Year = newYear
        def setPrice(self, newPrice):
            self._price = newPrice
        #create getters
        def getName(self):
            return self._Name
        def getMake(self):
            return self._Make
        def getModel(self):
            return self._Model
        def getYear(self):
            return self._Year
        def getPrice(self):
            return self._price
        #Create behaviors
        #Determine the cars age
        def carAge(self):
            '''Description: This method is designed to calculate the age of the car
            Parameters:
                carYear(int): contains the year the car was manufactured
                curYear(int): contains the current year
            Return:
                age(int): Contains the age of the car
            '''
            #get cars year
            carYear = self._Year
            #get the current year
            curYear = int((datetime.now()).year)
            #calculate the age by subtracting datetimeobjects and then dividing by 365
            age = (curYear - carYear)
            return age
        #Compute the sales tax(5%) and state tax(2%)
        def taxes(self):
            '''Description: This method is designed to calculate the taxes due
            Parameters:
                price (int): contains the price of the car
                sales (flt): Calculates the sales tax
                state (flt): Calculates the state tax
            Return:
                total (flt): calculates the total for sales and state taxes
            '''
            #Get price
            price = self._price
            #calculate taxes
            sales = price * .05
            state = price * .02
            #Get the total
            total = sales + state
            return total
        def depreciation(self):
            '''Description: This method is designed to calculate the depreciation of a vehicle
            Parameters:
                age (int): contain the cars age
                price(int): contain the cars price
            Return:
                price(int): the depreciated price of the car
            '''
            age = self.carAge()
            price = self._price

            while age > 0:
                age -= 3
                price -= (price * .10)
            if price < 0:
                    total = 0
            return price
        #create tostring
        def __str__(self):
            return f'''
            The cars Name is {self._Name}
            The cars Make is {self._Make}
            The cars Model is {self._Model}
            The cars Year is {self._Year}
            The cars price is {self._price}
            '''
#Get the instance
carInstance = Car()
#Get the variables and check them
carName = input('What is the cars name? ')
carMake = input('What is the cars make? ')
carModel = input('What is the cars model? ')
carYear = input('What is the cars year? ')
while True:
    try:
        carYear = int(carYear)
        break
    except Exception:
        print('Invalid input please try again')
        carYear = input('What is the cars year? ')
carPrice = input('What is the cars Original price? ')
while True:
    try:
        carPrice = int(carPrice)
        if carPrice < 0:
            raise ValueError
        break
    except Exception:
        print('Please input a real price')
        carPrice = input('What is the cars Original price? ')
#Run the setters and getters
carInstance.setName(carName)
print(f'The cars name was {carInstance.getName()}')
carInstance.setMake(carMake)
print(f'The cars make was {carInstance.getMake()}')
carInstance.setModel(carModel)
print(f'The cars model was {carInstance.getModel()}')
carInstance.setYear(carYear)
print(f'The cars year was {carInstance.getYear()}')
carInstance.setPrice(carPrice)
print(f'The price of the car was {carInstance.getPrice()}')
#Run behaviors
print(f'The cars age is {carInstance.carAge()}')
print(f'The total taxes due is {carInstance.taxes()}')
print(f'After depreciation the car is worth {carInstance.depreciation()}')
print()
#Print the tostring
print(carInstance)