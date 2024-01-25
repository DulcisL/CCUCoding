#Class Library
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


#take all data from the user
#create an inherited instance of class (object)
#make a list of objects and print a list
