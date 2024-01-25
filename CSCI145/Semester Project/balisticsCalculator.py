''' Name: Lakota Dolce4444
Date:
Assignment: Semester Project Part C
Pseudocode (as needed):
'''
#Imports
from adminFile import *
from LinkedListServices import *
from SortFile import *

#Set up login
def login(choice = 0):
    '''Description: This method is designed to set up a login for the user
        Parameters:
            choice (int): Contain the users choice used in the menus
            passcode (int): Contain the admin passcode
        Return:
            nothing
        '''
    
    while True:
        print('Welcome')
        print('''If you would like to enter as an Administrator enter 1
        Enter 2 for Standard User options
        Enter 3 for History
        Enter 4 to create / view a range card
        Enter 9 if you would like to quit''')
        try:
            #Check choice input
            choice = int(input('\n'))
            #Check for quitting parameters
            if choice == 9:
                print('Goodbye')
                quit()
            #All other options
            if choice == 1:
                try:
                    # require a password for access to the admin side
                    # Administrator would be allowed to change default values used in the calculations as well as normal functions of the user
                    password = int(input('Please enter the 4 digit passcode (1234): '))
                    #Check password
                    if password != 1234:
                        raise ValueError
                    if password == 1234:
                        #Print admin menu
                        print('Welcome Administrator')
                        print('''What would you like to do?
                        1) Change default values for calculations
                        2) Run the menu             
                        ''')
                        #Create admin instance
                        admin = Admin()
                        try:
                            #Take admin choice from menu and complete action
                            adminChoice = int(input('Enter your choice here: '))
                            if adminChoice == 1:
                                admin.changeVarDefaults()
                            if adminChoice == 2:
                                #Run the next menu and the calculator
                                print(admin)
                                history.addNode(admin.getDrop())
                            else: raise ValueError
                        except Exception:
                            #Tell user what went wrong
                            print('Not a valid input')
                        
                except Exception:
                    #Tell user what went wrong
                    print("You entered an incorrect passcode")
                    continue
            if choice == 2:
                #Create standard user instance
                user = User()
                #Run the next menu and the calculator
                print(user)

                #keep track of history
                history.addNode(user.getDrop())

            if choice == 3:
                #Check if there is history
                if history.getHead() != None:
                    print('The previous drop values from lowest to highest are:  ')
                    #history.printNode()

                    #get history and store in a list
                    ulist = []
                    history.iterate(ulist)

                    newlist = []
                    #get drop from each item
                    for item in ulist:
                        newlist.append(item.getDrop())

                    #sort the list
                    sort = Sort()
                    sort.selectionSort(newlist)

                    for item in newlist:
                        print(f'{item} inches ')

                if history.getHead() == None:
                    print('There is no history')

            if choice == 4:
                user = User()
                user.rangeCard()

        except Exception:
            #Tell user what went wrong
            print('You entered an invalid input please try again')

#Create linked list instance

history = LinkedList()
#Call the login
login()
#Program close
print('Good Luck')