# Pseudocode
# Pseudocode is an artificial and informal language that helps programmers
# develop algorithms. Pseudocode is a "text-based" detail (algorithmic) design tool.
# The rules of Pseudocode are reasonably straightforward.
# All statements showing "dependency" are to be indented.
# These include while, do, for, if, and switch.
# Steps
    # write a plan in plain English
    # then write in terms of structures (if, while, for)
    # write/ display / print are like print statements (output)
    # read is what you are taking in to the program (input)

# IPO
# Input Process Output
# Algorithm Design
# code origination
# Input
    # variables Declared first
    # take input from the user or external resource
#Process
    # body of code and calculations
    # structures, functions
    # main code of program and calculations
# Output
    # display information to the screen (i.e.. console)
    # display information in an external resource (i.e. .txt file)

# write a program to determine if the 5th character of a string is the letter c
# and place a - in the middle of the string.

# INPUT
    # Character of a string
    # Need a string to check and modify
        # Get string from user
        # INPUT Please enter a string
        #assign the string to a variable
        # yourString = INPUT
yourString = input('Please enter a string: ')

# PROCESS
    # Check for the letter c as the fifth character
    # and place a - in the middle of the string
    # Evaluate a string
    # Create a function to check and modify a string
        # FUNCTION - stringEvaluator(yourString)
def stringEvaluator(yourString) :
        # Check for a valid string
            # Check the length of the string
                # CHECK the string is > 0
                    # TRUE: Continue
                    # FALSE: Tell user Terminate
                # CHECK the string is >= 5
                    # TRUE: Continue
                    # FALSE: Tell user Terminate
        if len(yourString) <= 0 & len(yourString <= 5):
            print('You must enter a string larger than 5')
            #Break out of function
            return ''
        # MAKE string lowercase
        yourString.lower()
            # Is the string at 5 character
                # IS string character 5 == c
                    # TRUE: Tell the user a c is in index 5
                    #FALSE: Tell the user a c is not in index 5
        if yourString[4] == 'c':
            print('Tell the user a c is the fifth character')
        else:
            print('Tell the user a c is not the fifth character')
            # Add a - in the middle of the string
                # Find the len of the string
                # DIVIDE the len by 2
                # use that index as the middle
                    # Place first 1/2 in a variable called first
                    # Place second 1/2 in a variable called last
                    # CONCATINATE the first + '-' + last
                    # Save the results in newString
        # Return modified string
            # Return new string

# OUTPUT
    # Output to the console
        # Print the User string
        # Print the modified string

#End program

# change the program to write to a text file.