''' Name: Lakota Dolce
Date: 3/16/2023
Assignment: Wk 09 Assignment 1
Pseudocode:(when needed)
'''
class Class():
    '''Description: This class is to take in information about a class and to store multiple instances of itself
    Attributes:
        className (str): Stores the name of the class
        classNumber (int): Store the class number
        Classroom (str): Store the classroom for the class
        semester (str): Store the semester the class is taken
        credits (int): Store the number of credits the class is worth
        subject (str): Store the subject the class falls under
        classList (list): Store instances of itself 
    Behaviors:
        makeList: Create instances of the object and send them to be stored in itself
        appendList: Store the instances to the list
    '''
    #Attributes
    _className = str
    _classNumber = int
    _classroom = str
    _semester = str
    _credits = int
    _subject = str
    _classList = list

    #Make the initializer
    def __init__ (self, name: str, number: int, roomNumber: int, semester: str, credit: int, subject: str):
        self._className = name
        self._classNumber = number
        self._classRoom = roomNumber
        self._semester = semester
        self. _credits = credit
        self._subject = subject
        self._classList = []

    #Setters / Getters
    def setClassName (self,newName: str):
        self._className = newName
    def setClassNumber (self, newNumber: int):
        self._classNumber = newNumber
    def setClassroom (self, newRoom: str):
        self._classroom = newRoom
    def setSemester (self, newSemester: str):
        self._semester = newSemester
    def setCredits (self, newCredits: int):
        self._credits = newCredits
    def setSubject (self, newSubject: str):
        self._subject = newSubject
    def setClassList (self, overwrite: list):
        self._classList = overwrite

    def getClassName (self):
        return self._className
    def getClassNumber (self):
        return self._classNumber
    def getClassroom (self):
        return self._classroom
    def getSemester (self):
        return self._semester
    def getCredits (self):
        return self._credits
    def getSubject (self):
        return self._subject
    def getClassList (self):
        return self._classList

    #Actions

    #Make private appender 
    def _appendList (self, instance):
        '''Description: This method is designed to store class instances in a list inside the class
        Parameters:
            instance (obj): passes in the created instance to be appended to the list
        Return:
            nothing
        '''
        self._classList.append(instance)
    #Make the class list action
    def makeList (self):
        '''Description: This method is designed set up the instance to be stored in class list
        Parameters:
            none
        Return:
            nothing
        '''
        #Take in all how many classes the user wants to add
        try:
            #Set loop environment
            count = 1
            runs = int(input('How many classes do you have? '))
            while count <= runs:
                #Get and check the information for the class instance
                try:
                        name = input(f'Please enter the name for class {count}: ')
                        number = int(input('Please enter the class number: '))
                        room = input('Please enter the classroom: ')
                        semester = input('Please enter the semester: ')
                        credits = int(input('Please enter the amount of credits for the course: '))
                        subject = input('Please enter the subject: ')

                        #create the instance
                        classInstance = Class(name, number, room,semester, credits, subject)
                        
                        #call the appending method
                        self._appendList(classInstance)

                        count += 1
        #Explain to the user if there are any errors
                except Exception:
                    print("You didn't enter a usable input")
        except Exception:
            print('You have entered an invalid input please try again.')

    #Define the toString
    def __str__ (self):
        return f"""
        Class: {self._className} Number: {self._classNumber} Semester:  {self._semester}
        Credits: {self._credits}
        Subject: {self._subject}
        """

#Take all user data and check the information given 
while True:
    try:
        name = input('Please enter the name of the class: ')
        number = int(input('Please enter the class number: '))
        room = input('Please enter the classroom: ')
        semester = input('What semester is the class? ')
        credits = int(input('Please enter the number of credits for the class: '))
        subject = input('Please enter the subject for the class: ')

        #Break the loop when done
        break

    #Tell user what went wrong
    except Exception:
        print("Not a valid input try again.")

#Create the instance
schedule1 = Class(name, number, room, semester, credits, subject)

#Print current class
print(f'The class is {schedule1}')

#test the object
#Test all inputs
while True:
    try:
        schedule1.setClassName(input('Please enter a new class name: '))
        print('The class name is ', schedule1.getClassName())
        schedule1.setClassNumber(int(input('Please enter a new class number: ')))
        print('The class number is ', schedule1.getClassNumber())
        schedule1.setClassroom(input('Please enter the new class room: '))
        print('The class room is ', schedule1.getClassroom())
        schedule1.setSemester(input('Please enter the new semester: '))
        print('The semester is ', schedule1.getSemester())
        schedule1.setCredits(input('Please enter the new credit amount: '))
        print('The new credit amount is ', schedule1.getCredits())
        schedule1.setSubject(input('Please enter the new class subject: '))
        print('The subject is ', schedule1.getSubject())
        schedule1.setClassList(list(input('Please enter something to overwrite the list: ')))
        print('The list is ', schedule1.getClassList(), '\n')
        #Reset list to nothing
        schedule1.setClassList([])

        #Print the new class
        print(f'The new class is {schedule1}')

        #Break the loop when done
        break
    except Exception:
        print('Not a valid input, try again \n')

# Complete the actions and create a class list
schedule1.makeList()

#Set loop environment and print information
count = 1
classList = schedule1.getClassList()
for schedule in classList:
    print(f'Class {count} is {schedule}')
    count += 1