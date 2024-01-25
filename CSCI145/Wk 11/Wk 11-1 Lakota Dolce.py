import portfolioFile as portfolio

def getAccount():
    '''Description: This method is designed to get the account the user wishes to use
        Parameters:
            none
        Return:
            account (int): contains the integer linked to the account the user wants to access
    '''
    # Print the menu for the getting account
    print('\nIf you would like to access the checking please enter 1')
    print('If you would like to access your savings please enter 2')
    # Take and check user input
    while True:
        try:
            choice = int(input('Please enter here: '))
            if choice >= 1 and choice <= 2:
                if choice == 1:
                    # Set the variables
                    return 'Checking'
                if choice == 2:
                    # Set the variables
                    return 'Savings'
            else:
                raise ValueError
        except Exception:
            print('You entered an invalid choice, please try again')


def getAmount (transaction):
    '''Description: This method is designed to get the amount the use wants to add, subtract or transfer from their account
        Parameters:
            none
        Return:
            amount (float): contains the amount the user wishes to use
    '''
    while True:
        try:
            amount = round(float(input('\nPlease enter the amount that you wish to use: ')), 2)
            # Check for a posotive number
            if amount < 0:
                raise ValueError
            if amount > 0:
                return amount
        except Exception:
            print('You did not enter a valid amount, please try again')

def getTransaction ():
    '''Description: This method is designed to get the transaction the user wishes to complete
        Parameters:
            none
        Return:
            transaction (int): contains an integer linked to the transaction the user wishes to do
    '''
    #Print the menu
    print('\nIf you want to withdraw please enter 1')
    print('If you want to deposit please enter 2')
    print('If you want to transfer from the account please enter 3')
    print('If you want to see your balance enter 4')
    #Get and check the users choice
    while True:
        try:
            transaction = int(input('Please make your choice here: '))
            if transaction >0 and transaction <= 4:
                return transaction
            else:
                raise ValueError
        except Exception:
            print('Not a valid choice please try again')

def makeTransaction(account: str, transaction: int, amount: float = 0):
    '''Description: This method is designed to call the correct methods for the user
        Parameters:
            amount (float): contains the amount the user wants to withdraw
            account (str): contains the account the user wishes to use
            transaction (int): contains the integer linked to the transaction wanted
        Return:
            nothing
    '''
    #check the transaction and call the correct method
    if transaction == 1:
        portfolio1.withdraw(amount, account)
    if transaction == 2:
        portfolio1.deposit(amount, account)
    if transaction == 3:
        portfolio1.transfer(amount, account)
    if transaction == 4:
        print(f'{account} has ${portfolio1.getBalance(account)}')

portfolio1 = 0
while True:
    try:
        print('\n-----Welcome to the Bank----- \n')
        print('What is your initial checking account value?')
        checkingAmount = round(float(input('Please enter the initial account amount: ')), 2)
        print('What is your initial savings account value?')
        savingsAmount = round(float(input('Please enter the initial account amount: ')), 2)
        #Check the amounts and create instance
        if checkingAmount >= 0 and savingsAmount >= 0:
                        portfolio1 = portfolio.Portfolio(checkingAmount, savingsAmount)
                        break
        else: raise ValueError
    except Exception:
        print('A valid amount was not entered, please try again')

while True:
    #Set up the initial values in the instance
    print('-----Welcome to the Bank----- \n')
    #Get and check user input
    while True:
        try: 
            account = getAccount()
            transaction = getTransaction()
            if transaction != 4:
                amount = getAmount(transaction)
                makeTransaction(account, transaction, amount)
            if transaction == 4:
                makeTransaction(account, transaction)
            print(f'\n{portfolio1}')
            break
        except Exception:
            print('An error occurred please try again')