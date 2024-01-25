''' Name: Lakota Dolce
Date: 3/22/2023
Assignment: Wk 10 Assignment 2
Pseudocode:(when needed)
'''


class Person ():
    '''Description: This class is to take in information about a person, change a specific class,
                        and calculate the year of birth of the person
    Attributes:

    _name (str): Contains the persons name
    _age (int): Contains the persons age
    _height (int): Contains the persons height
    _Classes (list): contain the classes the person is enrolled

    Behaviors:

    classChange -> Change a specific class in the list
    getYOB -> Gets the year of birth of the person
    '''
    # Attributes
    _name = str
    _age = int
    _height = int
    _classes = list

    # Constructor
    def __init__(self, name: str, age: int, height: int, classes: list):
        self._name = name
        self._age = age
        self._height = height
        self._classes = classes

    # Setters and getters
    def setName(self, name: str):
        self._name = name

    def setAge(self, age: int):
        self._age = age

    def setHeight(self, height: int):
        self._height = height

    def setClasses(self, classes: list):
        self._classes = classes

    def getName(self):
        return self._name

    def getAge(self):
        return self._age

    def getHeight(self):
        return self._height

    def getClasses(self):
        return self._classes

    # Actions
    def classChange(self):
        '''Description: This method is designed to change a specific class in a list
        Parameters:
            currentClasses (list): Contains the list of classes to change
            placeChange (int): The item in the list that needs to be changed
            change (str): New Class being changed to
        Return:
            self.classes (list): Updated list of classes enrolled
        '''
        currentClasses = self._classes
        count = 1
        # print out the options
        for classes in currentClasses:
            print(f'Class {count}: {classes}')
            count += 1
        # check user input and change the class
        while True:
            try:
                # get the class that needs changed
                placeChange = int(
                    input('Please enter the number for the class that needs to changed: ')) - 1
                # get the new class
                change = input('Please enter the new class to be changed to: ')
                # Change the class in the list
                print(f'Change item {placeChange} to {change}')
                currentClasses[placeChange] = change
                # Set the class with setter
                self.setClasses(currentClasses)
                # break the loop
                break
            except Exception:
                # tell the user what went wrong
                print('You entered an invalid input, please try again')

    def getYOB(self):
        '''Description: This method is designed to calculate the year of birth
        Parameters:
            age (int): contains the age of the person
            currentYear (int): contains the current year
        Return:
             str: contains the year the person was born
        '''
        currentYear = 2023
        age = self._age
        return currentYear - age

    # String Method
    def __str__(self):
        return f'''{self._name} is {self._age} years old,
        has a height of {self._height} inches,
        and attends {self._classes}.\n
        '''


class Student (Person):
    '''Description: This class is to take information from the user and change the major, calculate years left
        Attributes:
            _major (str): contains the major of the person
            _EstimatedGradDate (str): contains the date the person is hoping to graduating
            _careerGoal (str): contains the career goal of the person
            _gpa (float): contains the accumulative grade of the person
        Behaviors:
            changeMajor -> allows the user to change the major of the person
            yearsLeft -> allows the user to calculate years left
            increaseGPA -> increases the gpa by 2%
            decreaseGPA -> decrease the gpa by 10%
    '''
    # Attributes
    _major = str
    _estimatedGradDate = str
    _careerGoal = str
    _gpa = float

    # constructor
    def __init__(self, major: str, date: str, goals: str, gpa: float, name: str, age: int, height: int, classes: list):
        super().__init__(name, age, height, classes)
        self._major = major
        self._estimatedGradDate = date
        self._careerGoal = goals
        self._gpa = gpa

    # setters and getters
    def setMajor(self, major: str):
        self._major = major

    def setGradDate(self, date: str):
        self._estimatedGradDate = date

    def setCareerGoal(self, goal: str):
        self._careerGoal = goal

    def setGPA(self, gpa: int):
        self._gpa = gpa

    def getMajor(self):
        return self._major

    def getGradDate(self):
        return self._estimatedGradDate

    def getCareerGoals(self):
        return self._careerGoal

    def getGPA(self):
        return self._gpa

    # Actions
    # Change the major
    def changeMajor(self):
        '''Description: This method is designed to change the major of the student
            Parameters:
                newMajor (str): contains the new major from user input
            Return:

        '''
        while True:
            try:
                newMajor = input('Please enter the new major you would like to change to: ')
                if len(newMajor) > 1:
                    self.setMajor(newMajor)
                    break
                if len(newMajor) < 1:
                    raise ValueError
            except Exception:
                print('Please enter a usable input')
                return

    # Calculate the time left
    def yearsLeft(self):
        '''Description: This method is designed to calculate the years left for the degree path
            Parameters:
                curYear (int): contains the current year
                gradDate (str): contains the templated graduation date of the student
            Return:
                timeLeft (int): the time the student has left before graduation
        '''
        while True:
            try:
                #set current year
                curYear = 2023
                #Get Grad date
                gradDate = self._estimatedGradDate
                #Get the year
                gradDate = int(gradDate[-4:])
                #calculate
                return gradDate - curYear
            except Exception:
                #If input was wrong, catch it now and re=enter
                print('Invalid Date input, please re-enter')
                gradDate = input('Please enter the expected graduation date in mm/dd/yyyy format: ')
                self.setGradDate(gradDate)

    # Increase the GPA by 2%
    def increase(self):
        '''Description: This method is designed to increase the GPA by 2%
            Parameters:
                curGPA (float): contains the current gpa
                newGPA (float): contains the new gpa
            Return:
                newGPA (float): contain the new gpa
        '''
        # Get GPA
        curGpa = self._gpa
        #Calculate with a 2% increase
        newGpa = curGpa * 1.02
        #Return the new GPA
        return newGpa
    
    # Decrease the GPA by 10%
    def decrease(self):
        '''Description: This method is designed to decrease the GPA by 10%
            Parameters:
                curGPA (float): contains the current gpa
                newGPA (float): contains the new gpa
            Return:
                newGPA (float): contains the new gpa
        '''
        # Get the GPA
        curGpa = self._gpa
        #Calculate the 10% decrease
        newGpa = curGpa * .9
        #Return the new GPA
        return newGpa
    # string method

    def __str__(self):
        return f''' {super().__str__()}
        The major is {self._major}
        The estimated graduation date is {self._estimatedGradDate}
        The career goals are {self._careerGoal}
        The current GPA is {self._gpa}
        '''


# get and test the information:
while True:
    try:
        name = input("Please enter your name: ")
        age = int(input('Please enter your age: '))
        height = int(input('Please enter your height in inches: '))
        classes = []
        classNum = int(input('How many classes are you enrolled in? '))
        while classNum > len(classes):
            classAdd = input('Please enter your class: ')
            classes.append(classAdd)
        major = input('Please enter your major: ')
        estimatedGradDate = input(
            'Please enter the expected graduation date in mm/dd/yyyy format: ')
        careerGoal = input('Please enter a career goal: ')
        gpa = float(input('Please enter the current GPA: '))
        break
    except Exception:
        #Tell the user what went wrong
        print('You entered an unusable input, please try again.')

# Create the instance
student1 = Student(major, estimatedGradDate, careerGoal,
                   gpa, name, age, height, classes)

# Test the object and parent
print(f'Current student: {student1}')

# Student testing
student1.changeMajor()
print(f'The new Major is: {student1.getMajor()}')
print(f'{student1.getName()} has {student1.yearsLeft()} years left')
print(
    f' The current GPA is {student1.getGPA()} after a 2% increase it is now {student1.increase()}')
print(
    f' The current GPA is {student1.getGPA()} after a 10% decrease it is now {student1.decrease()}')

# Person class testing
student1.classChange()
print(f'The new student info is: {student1}')
print(f'The year the student was born is {student1.getYOB()}')
