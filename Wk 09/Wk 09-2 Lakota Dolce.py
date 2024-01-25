''' Name: Lakota Dolce
Date: 3/16/2023
Assignment: Wk 09 Assignment 2
Pseudocode:(when needed)
'''
#Create the class
class Item ():

    '''Description: This class is to take in information about a class and to store multiple instances of itself
    Attributes:
        itemName (str): Store the name of the item
        itemNumber (int): Store the UPC of the item
        itemSize (str): Store the size of the item
        itemPriceList (list): Store the price list of the item
        itemDesc (str): Store the items description
    Behaviors:
    '''

    #Attributes
    _itemName = str
    _itemNumber = int
    _itemSize = str
    _itemPriceList = list
    _itemDesc = str

    #make the initializer
    def __init__ (self, name: str, number: int, size: str, priceList: list, desc: str):
        self._itemName = name
        self._itemNumber = number
        self._itemSize = size
        self._itemPriceList = priceList
        self._itemDesc = desc

    #Setters and getters
    def setItemName (self, newName: str):
        self._itemName = newName
    def setItemNumber (self, newNumber: int):
        self._itemNumber = newNumber
    def setItemSize (self, newSize: int):
        self._itemSize = newSize
    def setItemPriceList (self, newPriceList: list):
        self._itemPriceList = newPriceList
    def setItemDesc (self, newDesc: str):
        self._itemDesc = newDesc

    def getItemName (self):
        return self._itemName
    def getUPC (self):
        return self._itemNumber
    def getItemSize (self):
        return self._itemSize
    def getItemPriceList (self):
        return self._itemPriceList
    def getItemDesc (self):
        return self._itemDesc

    #actions
    #overide the length method
    def __len__ (self):
        '''Description: This method is designed to override the len function
        Parameters:
            none
        Return:
            The item size
        '''
        #Set to item size
        return self._itemNumber

    #overide int method
    def __float__ (self):
        '''Description: This method is designed set up the instance to be stored in class list
        Parameters:
            none
        Return:
            The item number
        '''
        # get average
        average = 0
        for price in self._itemPriceList:
            average += float(price)
            average = average / 2

        #Set to item number
        return round(average, 2)

    #Make the string method
    def __str__ (self):
        return f'''The item is {self.getItemName()}, The Item Number(UPC) is {self.getUPC()}, The size is {self.getItemSize()}
        The price list is {self.getItemPriceList()}
        The Item description is {self.getItemDesc()}
        '''
#Get information and test the data for the right type
item1 = ''
while True:
    try:
        #Get the information from the user
        name = input('Please enter the name of the item: ')
        number = int(input('Please enter the only the number of the item number(UPC): '))
        size = input('Please enter the size of the item: ')
        
        #get the price list
        priceList = []
        while True:
            try:
                price = float(input('Please enter the price of the item or any letter to quit: '))
                priceList.append(round(price, 2))
            except Exception:
                break
        
        desc = input('Please enter a brief description of the item in one continuos line: ')
        
        #Create the instance and print it
        item1 = Item(name, number, size, priceList, desc)

        #break the loop
        break

    except Exception:
        #Tell the user what went wrong
        print('You entered an unusable value, please try again')

#Print instance
print(f'The instance is \n {item1}')

#Test the class
while True:
    #Test the user input
    try:
        item1.setItemName(input('Please enter the new item name: ')) 
        print(f'The new item name is {item1.getItemName()}')

        item1.setItemNumber(int(input(f'Please enter the new item number (UPC): ')))
        print(f'The new item number (UPC) is {item1.getUPC()}')

        item1.setItemSize(input('Please enter the new item size: '))
        print(f'The new size is {item1.getItemSize()}')

        #Get the list of prices
        priceList = []
        while True:
            try:
                price = float(input('Please enter the price of the item or any letter to quit: '))
                priceList.append(round(price, 2))
            except Exception:
                item1.setItemPriceList(priceList)
                break
        #Print the list of prices
        for price in item1.getItemPriceList():
            print(f'Price is {price}')
            
        item1.setItemDesc(input('Please enter the new item description (no new lines): '))
        print(f'The new description is {item1.getItemDesc()}')

        #break the loop
        break

    except Exception:
        #Tell user what went wrong
        print('You entered an invalid input, please try again')

print(f'''The overrides are
The len function as {len(item1)}, and
The float function as {float(item1)}
''')

print(f'''The new item is class is as follows:
{item1}''')