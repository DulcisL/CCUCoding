import bankAccountFile as bankAccount


class Portfolio ():
    '''Description: This class is to store all and overwrite the variables used for the calculator
    Attributes:

        _checking (obj): Contains the bank object as a checking account instance
        _savings (obj): Contains the bank object as a savings account instance

    Behaviors:

        deposit (amount(float), account(str)): allow the user to deposit into the specified account
        withdraw (amount(float), account(str)): allow the user to withdraw from the specified account
        transfer (amount(float), account(str)): allow the user to transfer from the specified account
        getBalance(amount(float), account(str)): allow the user to get the balance of the specified account
    '''

    # Attributes
    _checking = object
    _savings = object

    # constructor
    def __init__(self, checkingAmount: float = 0, savingAmount: float = 0):
        self._checking = bankAccount.Bank(checkingAmount)
        self._savings = bankAccount.Bank(savingAmount)

    # Behaviors
    def deposit(self, amount: float, account: str):
        '''Description: This method is designed to add the ammount to the account
        Parameters:
            amount (float): contains the amount the user wants to deposit
            account (str): contains the account the user wishes to use
        Return:

        '''

        # Check which account
        if account == 'Savings':
            # Get the new total
            newTotal = self._savings.getTotal() + amount
            # call the setter
            self._savings.setTotal(newTotal)
            print(f'The new total of {account} is ${float(self._savings)}')

        if account == 'Checking':
            # Get the new total
            newTotal = self._checking.getTotal() + amount
            # call the setter
            self._checking.setTotal(newTotal)
            print(f'The new total of {account} is ${float(self._checking)}')

    def withdraw(self, amount: float, account: str):
        '''Description: This method is designed to subract the ammount from the account
        Parameters:
            amount (float): contains the amount the user wants to withdraw
            account (str): contains the account the user wishes to use
        Return:
            1: signify Pass
            0: signify Fail
        '''

        # Check which account
        if account == 'Savings':
            # Get the new total
            newTotal = float(self._savings) - amount
            # check for overdraw
            if newTotal > 0:
                # call the setter
                self._savings.setTotal(newTotal)
                print(f'The new total of {account} is ${float(self._savings)}')
                return 1
            else:
                print('Account will be overdrawn enter a different amount')
                return 0
            
        if account == 'Checking':
            # Get the new total
            newTotal = float(self._checking) - amount
            # check for overdraw
            if newTotal > 0:
                # call the setter
                self._checking.setTotal(newTotal)
                print(
                    f'The new total of {account} is ${float(self._checking)}')
                return 1
            else:
                print('Account will be overdrawn please enter a different amount')
                return 0
        else:
            return 0

    def transfer(self, amount: float, account: str):
        '''Description: This method is designed to subract the ammount from one account and add it to the other
        Parameters:
            amount (float): contains the amount the user wants to withdraw from one account and add to the other
            account (str): contains the account the user wishes to use
        Return:
            1: signify Pass
            0: signify Fail
        '''

        # Check the account
        if account == 'Savings':
            # run withdraw and deposit for account
            # Check if withdraw passed
            if self.withdraw(amount, account) == 1:
                # Transfer balance
                self.deposit(amount, 'Checking')
                print(f'The new total of {account} is ${float(self._savings)}')
                return 1
            # Check if withdraw failed
            else:
                print('Transfer failed')
                return 0
            
        if account == 'Checking':
            # run withdraw and deposit for account
            # Check if withdraw passed
            if self.withdraw(amount, account) == 1:
                # Transfer balance
                self.deposit(amount, 'Savings')
                print(f'The transfer was completed')
                return 1
            # Check if withdraw failed
            else:
                print('Transfer failed')
                return 0
        else:
            return 0

    def getBalance(self, account: str):
        '''Description: This method is designed to display the ammount of an account
        Parameters:
            account (str): contains the account the user wishes to use
        Return:
        '''
        # Check the account
        if account == 'Checking':
            # Call the overrode float method
            return float(self._checking)
        if account == 'Savings':
            # Call the overrode float method
            return float(self._savings)
    
    # Make the string method
    def __str__ (self):
        return f'Checking total is ${float(self._checking)}, Savings total is ${float(self._savings)}'