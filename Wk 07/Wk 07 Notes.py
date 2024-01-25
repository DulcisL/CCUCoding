#Object Lecture objectives
#objects and variables
#classes vs Instance
#simple class definitions
#constructor - special method that creates new instances
#Methods (actions, behaviors) - a function within a class
#class attributes
#overloading

#create a thing class from lecture
class Thing():
    #define attributes
    value = 0
    #create the constructor
    def __init__(self, value):
        #Initialize the instance variable
        self.value = value
    #behaviors
    def showMe(self):
        print(f'value: {self.value}')

#create an instance
thing1 = Thing(5)
thing2 = Thing(10)
#call the instance
thing1.showMe()
thing2.showMe()
#print(thing2.showMe()) won't show anything because nothing is returned


#create a room object
class Room ():
    '''Description: This class is to model a room to and change the layout
    Attributes:
        size (int): The size of the room (hidden)
        color (str): The color of the room (hidden)
        shape (str): The shape of the room (hidden)
    Behaviors:
        paintTheRoom() -> to change the room color
        areaOfTheRoom() -> calculate the area fo a room
        addFurniture() -> add a desk, chair, or table
    '''
    #attributes
    _size = 0
    _color = ''
    _shape = ''
    #constructor - a method that executes when an instance(copy) of the object is created
    def __init__ (self):
        self._size = 30
        self._color = 'Blue'
        self._shape = 'Square'

    #getters and setters
    def getSize(self):
        return self._size
    def getColor(self):
        return self._color
    def getShape(self):
        return self._shape

    def setSize(self, size):
        self._size = size
    def setColor(self, color):
        self._color = color
    def setShape(self, shape):
        self._shape = shape

    #actions
        #string method(to-string) / toString
    def paintTheRoom(self, newRoomColor):
        '''Description: This method is designed to change the paint in the room
        Parameters:
            newRoomColor (str): the color to change to
        Return:
            nothing
        '''
        print('Painting room ....')
        print(f'Current color {self._color}.. painted to {newRoomColor}')
        self.setColor(newRoomColor)
        print(f'The new room color is {self._color}')


    #compute the area of the room
    def areaOfRoom (self):
        '''Description: This method is designed to calculate the area of a room
        Parameters:
        length (int): length of the room in inches
        width (int): width of the room in inches
        Return:
        int - the area of the room in inches
        '''
        length = 10
        width = 20
        height = 40
        return length * width * height
    #helper Methods
    '''Description: This method to add a furniture item to the list
    Parameters:
    item (str) - the item to add to the furniture list
    Return:
    None
    '''
    #toString method
        #must return a string
    def __str__(self):
        return f'Room Size is {self._size}, Color is {self._color}, Shape is {self._shape}'

#test
room1 = Room()
print(room1)

#run setters
room1.setColor("Red")
print(room1)


#test the object
#ask the user for values to complete constructor
userColor = 'Purple' #input('Enter a room color: ')
userSize = 50
userShape = 'Octagonal'
#create an instance of the object
#declare a variable and set it equal to the class name with initializers ()
room2 = Room()
room2.setColor(userColor)
print(room2)

#store values in all attributes
#change the floorType to hardWood
#using getters and setters
room2.setColor(userColor)
room2.setSize(userSize)
room2.setShape(userShape)
#test the attributes and describe
currentColor = room2.getColor()
print(f'Current color is: ', currentColor)
# or
print(f'Current room size is: ', room2.getSize())
#etc for all setters/getters
#test behaviors
print(f'The area of the room is: ', room2.areaOfRoom())


#allow the user to change the floor type

#print all variables
#using toString method
#call method

#creating multiple rooms