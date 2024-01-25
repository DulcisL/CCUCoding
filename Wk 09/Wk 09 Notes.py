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
    #attributes set default types
    _size = int
    _color = str
    _shape = str
    _furnitureList = list
    _roomInstanceList = list

    #constructor - a method that executes when an instance(copy) of the object is created
    def __init__ (self, size: int, color: str, shape: str):
        self._size = size
        self._color = color
        self._shape = shape
        self._furnitureList = []
        self._roomInstanceList = []

    #getters and setters
    def getSize(self):
        return self._size
    def getColor(self):
        return self._color
    def getShape(self):
        return self._shape
    def getFurnitureList (self):
        #returns the entire list
        return self._furnitureList
    def getRoomInstanceList (self):
        return self._roomInstanceList

    def setSize(self, size: int): # Can set the type the object is supposed to be
        self._size = size
    def setColor(self, color: str):
        self._color = color
    def setShape(self, shape: str):
        self._shape = shape
    def setFurnitureList (self, furnitureList: list):
        #replaces the list
        self._furnitureList = furnitureList
    def setRoomInstanceList (self, roomInstance: list):
        self._roomInstanceList = roomInstance

    #actions
    def addMultipleInstancesToList (self):
        '''Description: This method is designed to store class instances in a list inside the class
        Parameters:
            none
        Return:
            nothing
        '''
        try: # usable outside of class or inside a class just have to change the variables
            numberOfRooms = int(input('How many rooms do you want to create? '))
            # after user enters data correctly write the rest of code here
            count = 1
            while count <= numberOfRooms:
                try:
                    self._size = int(input(f'Enter the size of room {count}: '))
                    self._color = input('Enter the room color: ')
                    self._shape = input('Enter the room shape: ')
                    roomInstance = Room(self._size, self._color, self._shape)
                    self._roomInstanceList.append(roomInstance)
                except:
                    print(f'You must enter a number for  room {count}')
                count += 1
        except:
            print("You must enter a number")

    def printFurnitureList (self):
        for furniture in self._furnitureList:
            print(f'Piece: {furniture}')
    #override the length and int
    def __len__(self):
        return self._size
    def __int__ (self):
        return self._size
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
    #helper Method
    def _addFurnitureToList(self, item: str): # private method
        '''Description: This method is the helper method that adds a furniture item to the list
        Parameters:
        item (str) - the item to add to the furniture list
        Return:
        completed (Boolean): determine if the item was added to the list
        '''
        self._furnitureList.append(item)
        return True
    def addFurniture (self, item: str): #created to call the private method
        '''Description: This method to add a furniture item to the list
        Parameters:
        item (str) - the item to add to the furniture list
        Return:
        None
        '''
        self._addFurnitureToList(item)

    # string method(to-string) / toString
    #toString method
    #must return a string
    def __str__(self):
        return f'Room Size is {self._size}, Color is {self._color}, Shape is {self._shape}'

#test
room1 = Room(20, 'Red', 'Square')
print(room1)

#run setters
room1.setColor("Red")
print(room1)

#the variable room1 is the object
#the = Room() is creating an instance
room1.setColor('Red')
room1.setSize(30)
room1.setColor('Yellow')
print(room1)
print(int(room1))
print(len(room1))

#private methods
#complete methods in room class
#create  list of rooms in class
print('---------Room 1 ----------')
room1.addFurniture('Chair')
room1.addFurniture('Couch')
room1.addFurniture('Desk')
room1.printFurnitureList()
print('---------Room 2 ----------')
#create multiple instances
room2 = Room(100, 'Green','Square')
room2.addFurniture('Table')
room2.addFurniture('Lamp')
room2.addFurniture('Counter')
room2.printFurnitureList()

# create a list of Room instances (object variables)
roomInstanceList = []
# ask the user to create rooms
# ask the user how many rooms to create
room2.addMultipleInstancesToList()
roomInstanceList = room2.getRoomInstanceList()
# add these rooms to a list
# print the instance list and print the class object
if len(roomInstanceList) > 0:
    count = 1
    for room in roomInstanceList:
        print(f'Room {count} is {room}')
        count += 1
# print room 2 and all data associated
print('Only Room 2 is ',roomInstanceList[1])