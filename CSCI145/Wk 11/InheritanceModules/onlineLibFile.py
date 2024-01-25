#Import the main class for inheritance
from libraryFile import *
#create an inherited class
# (Library) is the class inherited
class OnlineLib (Library):
    #Attributes

    _url = str
    _searchItem = str

    #Constructor
    def __init__ (self, url: str, name: str, numberOfBooks: int, librarian: str, open: bool = True):
        # Initializes the attributes of the parent class Library
        super().__init__(name, numberOfBooks, librarian, open)
        self._url = url
        self._searchItem = ''

    #Getters / setters
    def setUrl (self, url: str):
        self._url = url
    def setSearchItem (self, searchItem: str):
        self._searchItem = searchItem
    def getUrl (self):
        return self._url
    def getSearchItem (self):
        return self._searchItem
    #Actions

    #Chatbot
    def chatBot (self):
        print('Start Chatbot')
    #search
    def searchLib (self):
        print(f'Searching {self._searchItem}')

    # override checkedOutBooks form Library(parent) class
    def checkOutBook(self):
        #Set up a shopping cart to add multiple books
        print("You checked out Book 1")

    #String Method
    def __str__ (self):
        return f'Welcome to: {super().__str__()}. The URL is: {self._url}'
