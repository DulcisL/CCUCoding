#copy ObjectLecture Library Class
#derived class (Child) - a class that uses a base class or main class
#Must call parent constructor or call to super().__init__()

#overloading from base class (Parent)
#why use inheritance (reduce code and reduce your efforts)
#changes in parent happen to all children

# a class Library
class Library ():
    # has a name, numberOfBooks, librarian and optional open.
    _name = str #defines a string
    _numberOfBooks = int #defined as an integer
    _librarian = str
    _open = bool # defines a boolean
    _booksCheckedOut = list #defines an empty list

#Supply an appropriate constructor
#attributes with data types name: str
    #The open is optional
    #If the value is not set when the constructor initializes, the value to true
    def __init__(self, name: str, numberOfBooks: int, librarian: str, open = True):
        #initialize instance variables
        self._name = name
        self._numberOfBooks = numberOfBooks
        self._librarian = librarian
        self._booksCheckedOut = []
        self._open = open

    #getters
    def getName(self):
        return self._name
    def getNumberOfBooks(self):
        return self._numberOfBooks
    def getLibrarian(self):
        return self._librarian
    def getOpen(self):
        return self._open
    #setters
    def setName(self,name):
        self._name = name
    def setNumberOfBooks(self, numberOfBooks):
        self._numberOfBooks = numberOfBooks
    def setNLibrarian(self, librarian):
        self._librarian = librarian
    def setOpen(self, open):
        self._open = open

    #actions, methods, behaviors
    #checkOutBook(str bookName)
    #assumption any book is avaliable that is not currently checked out

    def checkOutBook(self, bookName: str):
        '''Description: This method is designed to add a book to the library house object list
        Parameters:
            bookName (str): contains the name of the book to checkout
        Return:
            (str) - To give the status of adding the book
        '''
        #check if book is already checked in
        if bookName in self._booksCheckedOut:
            return 'Sorry that book is checked out, try another.'
        else:
            self._booksCheckedOut.append(bookName)
            return f'{bookName} is checked out.'

    #printBooksCheckedOut()
    # Book 1: name
    # Book 2: name
    # Book 3: name
    # .....
    def printBooksCheckedOut(self):
        '''Description: The method is desgined to print the books checked out
        Parameters:
            none
        Return:
            nothing
        '''
        bookCount = 1
        for book in self._booksCheckedOut:
            print(f'Book {bookCount} {book}')
            bookCount += 1
        #to string (print method)
        # a print method that prints the following
        #------- Library name entered ----------
        # Number of books:
        # The Librarian is:
        #
    def __str__(self):
        return f'Library Name: {self._name} -> Number of Books: {self._numberOfBooks} -> Open: {self._open}'

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

#take all data from the user
#create an inherited instance of class (object)
#make a list of objects and print a list

#create an object of OnlineLib
url = input('Enter a url:')
name = input('Enter a name for the library: ')
numberOfBooks = int(input('Enter the number of books: '))
librarian = input('Who is the librarian? ')

ebsco = OnlineLib (url, name, numberOfBooks, librarian, False)

#Testing all the behaviors
ebsco.chatBot()
ebsco.searchLib()
ebsco.printBooksCheckedOut()
ebsco.checkOutBook()

print(ebsco)