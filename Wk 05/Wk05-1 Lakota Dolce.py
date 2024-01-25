''' Name: Lakota Dolce
Date: 2/08/2023
Assignment: Wk 05 Assignment 1
Pseudocode:
INPUT:
    Ask the user for a number
        INPUT Please Enter an integer:
            Store as variable userNumber

PROCESS:
    Create a function to count the number of digits in the number
    DEFINE digitCounter
        BASE CASE
            When the string containing the number is empty
            return the counter
        RECURSIVE CASE
            modify the string to take off a digit
            add to the counter
            RETURN with the modified string to the method
OUTPUT:
    PRINT the number of digits in the number
'''

counter = 0
'''Description: This method is designed to modify a string to count how many digits are in the number given
        Parameters:
            userNumber (str): A string containing the number the user entered
            count (int): the counter for the digits
        Return:
            counter (int): the final count for how many digits were in the number
'''
def digitCounter (userNumber):
    global counter
    #Base Case is when the string is empty
    if userNumber == '':
        return counter
    #Recursive case is when the string is not empty
    else:
        #modify the string
        userNumber = userNumber[1:]
        #add to the counter
        counter += 1
        #start method again with new string
        return digitCounter(userNumber)

#Take the users number
userNumber = input('Please enter an integer: ')

#Check the users input
while True:
    try:
        int(userNumber)
        #run the method
        copyUser = userNumber
        digits = digitCounter(userNumber)
        break
    except Exception:
        print('Incorrect input please try again')
        userNumber = input('Please enter an integer: ')

#print the results to the console
print(f'Your number was {copyUser}\n')
print(f'There are {digits} digits in that number')