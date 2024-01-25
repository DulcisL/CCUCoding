''' Name: Lakota Dolce
Date: 23JAN2023
Assignment: Wk-03 Assignment 2
Pseudocode:

INPUT:

Get a list of numbers
    Ask user for numbers until finished
        Ask user to enter a number or q to quit
            STORE as variable number

PROCESS:

        Set up loop environment
            Set sentinel variable
                VARIABLE stop = False
            Set list variable
                VARIABLE userNumbers = empty list
            Set counter
                VARIABLE runs = start at 0
        Create loop
            WHILE stop == False
                Add to counter
                    runs += 1
                Read number variable
                    INPUT:
                Determine if user wants to quit
                    TRUE: if user input 'q' terminate the program
                        set stop = True
                    FALSE: continue the program
                Add numbers to the list
                    CONVERT to integer
                    APPEND list with numbers
        Create text file

OUTPUT:

Write numbers to a text file with a description
    Create loop environment
        FOR x in range of the length of the list
        Describe what each number is and store in a variable
            STORE as numbersDesc
                numbersDesc = Number (x + 1 ) => index into number x variable
        Write to text file

'''
# Set up sentinel variable and list variable
stop = False
userNumbers = []
run = 0
# create continous loop
while stop == False:
    # Ask for the user input
    run += 1
    number = input(f'Enter number {run} or enter q to quit: ')
    # Check string
    if len(number) <= 0:
        continue
    elif number == 'q':
        stop = True
        break
    elif number != 'q':
        if number.isnumeric() == True:
            userNumbers.append(int(number))
        else:
            continue
# Create text file and write to it with for loop
# Create for loop to iterate through list
myFile = open('myfiles.txt', 'a')
for x in range(len(userNumbers)):
    # Send to text file
    numbersDesc = (f'Number {(x + 1)} => {userNumbers[x]} \n')
    myFile.write(numbersDesc)
myFile.close()
