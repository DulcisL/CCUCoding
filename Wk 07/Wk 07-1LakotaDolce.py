''' Name: Lakota Dolce
Date: 2/22/2023
Assignment: Wk 07 Assignment 1
Pseudocode:(when needed)
'''
from datetime import datetime, timedelta

class Person ():
    '''Description: This class is to model a persons personal information and to determine how long they have
    been employed, if they are due for an eval and to calculate a 5% raise
    Attributes:
        fullName (str): contains the persons full name
        emailAddress (str): contains the persons email address
        yearOfBirth (int): contains the persons year they were born
        phoneNumber (str): contains the persons phone number
        favoriteColor (str): contains the persons favorite color
        placeOfEmployment (str): contains the company the person is employed
        salary (int): contains the yearly salary of the person
        employmentStartDate (str) contains the starting date of most recent employment
        evaluationDate (str): contains the last time the person was evaluated
    Behaviors:
        addRaise() -> Change the users salary with a 5% increase
        lengthOfEmployment -> Calculate the length the person has been employed
        evalCheck -> Check if the person needs to be evaluated
    '''
    #Attributes
    _fullName = ''
    _emailAddress = ''
    _yearOfBirth = 0
    _phoneNumber = ''
    _favoriteColor = ''
    _placeOfEmployment = ''
    _salary = 0
    _employmentStartDate = ''
    _evaluationDate = ''
    #initialize
    def __init__ (self):
        self._fullName = ''
        self._emailAddress = ''
        self._yearOfBirth = ''
        self._phoneNumber = '0123456789'
        self._favoriteColor = ''
        self._placeOfEmployment = ''
        self._salary = 0
        self._employmentStartDate = '0000/00/00'
        self._evaluationDate = '0000/00/00'
    #Setters for changing values
    def setName (self, newName):
        self._fullName = newName
    def setEmail (self, newEmail):
        self._emailAddress = newEmail
    def setYOB (self, newYear):
        self._yearOfBirth = newYear
    def setPhone (self, newPhone):
        self._phoneNumber = newPhone
    def setColor (self, newColor):
        self._favoriteColor = newColor
    def setEmployment (self, newEmployment):
        self._placeOfEmployment = newEmployment
    def setSalary (self, newSalary):
        self._salary = newSalary
    def setStart(self,newStart):
        self._employmentStartDate = newStart
    def setEval(self, newEval):
        self._evaluationDate = newEval
    #Getters for getting values
    def getName (self):
        return self._fullName
    def getEmail (self):
        return self._emailAddress
    def getYOB (self):
        return self._yearOfBirth
    def getPhone (self):
        return self._phoneNumber
    def getColor (self):
        return self._favoriteColor
    def getEmployment (self):
        return self._placeOfEmployment
    def getSalary (self):
        return self._salary
    def getStart(self):
        return self._employmentStartDate
    def getEval(self):
        return self._evaluationDate

    #Behaviors
    #Add a 5% increase to salary
    def addRaise (self):
        '''Description: This method is designed to calculate a 5% raise
        Parameters:
            salary (int): current salary
            newSalary (flt): contain the salary with a 5% increase
        Return:
            nothing
        '''
        #Get the salary
        salary = self._salary
        #calculate the salary
        newSalary = float(salary) + (int(salary) * .05)
        #change the salary
        self.setSalary(newSalary)

    #Calculate the length of Employment
    def lengthOfEmployment (self):
        '''Description: This method is designed to count how long someone is employed
        Parameters:
            start (datetime): contains the start date of employment
            todaysDate (datetime): contains the current date
        Return:
            length(datetime): returns the number of days employed
        '''
        #get the start date
        start = self._employmentStartDate
        #get todays date
        todaysDate = datetime.now()
        #calculate the length between the two dates
        length = todaysDate - start
        length = length.days
        #return the difference
        return length

    #Check if the person needs an evaluation
    def evalCheck (self):
        '''Description: This method is designed to decide if an evaluation is due
        Parameters:
            lastEval (datetime): contains the date of the last evaluation
            todaysDate (datetime): contains todays date
        Return:
            due(str): a string that says yes or no depending on if the last eval was > a year ago
        '''
        #Get the last eval and convert to a usable input
        lastEval = self._evaluationDate
        #Get todays date
        todaysDate = datetime.now()
        #calculate the difference
        difference = todaysDate - lastEval
        #if last eval was >= a year prior they are due
        if int(difference.days) >= 365:
            due = 'Yes'
        #if not over a year ago eval is not due
        if int(difference.days) < 365:
            due = 'No'
        return due
    #define tostring
    def __str__(self):
        #set up return for all attributes
        return f'''
Full name is {self._fullName}
Email is {self._emailAddress}
Year of Birth is {self._yearOfBirth}
Phone number is {self._phoneNumber}
Favorite Color is {self._favoriteColor}
Place of employment is {self._placeOfEmployment}
Salary is {self._salary}
Employment start date was {self._employmentStartDate}
Last Evaluation was {self._evaluationDate}
'''

#Get the needed info and check the inputs
name  = input('Please enter your full name: ')
email = input('Please enter your email: ')
birthday = input('Please enter your birth year: ')
number = input('Please enter your phone number (only digits): ')
color = input('Please enter your favorite color: ')
employment = input('Please enter your employer: ')
salary = input('Please enter your yearly salary (only digits): ')
while True:
    try:
        salary = int(salary)
        break
        if len(salary) < 0:
            raise ValueError
    except Exception:
        print('Not a valid input, try again')
        salary = input('Please enter your yearly salary (only digits): ')
        continue
start = input('Please enter your employment start date (yyyy/mm/dd format): ')
while True:
    try:
        #convert to needed format
        start = datetime.strptime(start, "%Y/%m/%d")
        break
    except Exception:
        print('Not a valid input, try again')
        start = input('Please enter your employment start date (yyyy/mm/dd format): ')
        continue
eval = input('Please enter your last eval date (yyyy/mm/dd format): ')
while True:
    try:
        # convert to needed format
        eval = datetime.strptime(eval, "%Y/%m/%d")
        break
    except Exception:
        print('Not a valid input, try again')
        eval = input('Please enter your last eval date (yyyy/mm/dd format): ')
        continue

#Make the instance
person1 = Person()
#Run getters and setters
person1.setName(name)
print(f'The name given was {person1.getName()}')
person1.setEmail(email)
print(f'The email is {person1.getEmail()}')
person1.setYOB(birthday)
print(f'Their birthday is {person1.getYOB()} ')
person1.setPhone(number)
print(f'Their phone number was {person1.getPhone()}')
person1.setColor(color)
print(f'Their favorite color was {person1.getColor()}')
person1.setEmployment(employment)
print(f'They are employed at {person1.getEmployment()}')
person1.setSalary(salary)
print(f'Their salary is {person1.getSalary()}')
person1.setStart(start)
print(f'They started working there on {person1.getStart()}')
person1.setEval(eval)
print(f'Their last evaluation was {person1.getEval()}')
#test the behaviors
person1.addRaise()
print(f'Your new salary after a 5% raise is  {person1.getSalary()}')
print(f'You have been employed for {person1.lengthOfEmployment()} days')
print(f'You are due for a evaluation : {person1.evalCheck()}')
print()
#test the tostring
print(person1)