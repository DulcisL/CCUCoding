#program header
''' Name: Lakota Dolce
Date: 2/01/2023
Assignment: Wk 04 Assignment 1
Pseudocode:

INPUT:
User enters a choice from the menu

PROCESS:
Create a menu for the user with 3 choices
    Run menu in a while loop
        Sentinel variable run = BOOLEAN
    Read the user string and make sure that it is correct
        Use TRY, EXCEPT, and FINALLY
    Choice 1 create a calculator
        DEFINE QuizCalculator
            take user input for 2 numbers and the type they want to use
            Check inputs using TRY/ EXCEPT/ Finally
            Return an answer
    Choice 2 modify a string
        DEFINE stringModifier
            Read the user string and modify the string
                modify the string to be all capitals
                modify the string to have a '#' every fifth character
            Return the modified string
    Choice 3 quit the program
        Set while loop sentinel variable to False
    Print returned values to the console
OUTPUT:
'''

'''Description: This method is designed to calculate two numbers based on user input
        Parameters:
            x (int): contains the number the user has input
            y (int): contains the second number the user has input
            symbol (str): contains the operation the user wishes to do
        Return:
            total (int): The total of that sum
'''
def calculator(x,y,symbol):
    incorrectX = True
    incorrectY = True
    while incorrectX == True:
        try:
            x = int(x)
            incorrectX = False
        except ValueError:
            print('Incorrect input for the first number')
            x = input('Please enter first number again')
        finally:
            continue
    while incorrectY == True:
        try:
            y = int(y)
            incorrectY = False
        except ValueError:
            print('Incorrect input for the second number')
            y = input('Please enter second number again')
        finally:
            continue

    match symbol:
        case '+':
            value = x + y
        case '-':
            value = x - y
        case '*':
            value = x * y
        case '/':
            try:
                value = x / y
            except ZeroDivisionError:
                value = 'undefined'
                print('Cannot divide by zero')
        case _:
            value = 'none'
            print('Incorrect symbol input')
    return value

'''Description: This method is designed to read and modify a uses string
        Parameters:
            string (str): contains the user string
        Return:
            modifiedString (str): contains the modified string
'''
def stringModifier(string):
    try:
        modifiedString = string.swapcase()
    except:
        print('Your string case cannot be swapped')
        modifiedString = string
    finally:
        pound = 5
        while pound < len(string):
            modifiedString = modifiedString[:pound] + '#' + modifiedString[pound:]
            pound += 6
    return modifiedString

run = True
while run == True:
    userChoice = input('''
    Welcome to the menu
    Choose 1 for a basic calculator
    Choose 2 for a string modifier
    Enter any other character to quit
    Please enter your choice here: 
    ''')
    try:
        userChoice = int(userChoice)
    except ValueError:
        print('Goodbye')
        break
    finally:
        print('Good luck')

    if userChoice == 1:
        firstNumber = input('Please enter the first number: ')
        secondNumber = input('Please enter the second number: ')
        print('''Please enter the symbol,
        + to add
        - to subtract
        * to multiply
        / to divide 
        ''')
        symbol = input('Please enter your choice here: ')
        answer = calculator(firstNumber, secondNumber, symbol)
        print(f'The answer is {answer}')
        continue

    if userChoice == 2:
        userString = input('Enter a random string: ')
        modifiedString = stringModifier(userString)
        print(f'The modified string is: \n {modifiedString}')
        continue

    if userChoice != 1 or userChoice != 2:
        print('Goodbye')
        run = False

