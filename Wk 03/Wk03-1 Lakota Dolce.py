''' Name: Lakota Dolce
Date: 23JAN2023
Assignment: Wk-03 Assignment 1
Pseudocode:
Take a string and modify so to have an alternating pattern of
- every 2 characters
and ~ every 5th character

INPUT:

Need a string to read and modify
    Ask the user for a string
        INPUT = Enter a random string with no spaces:
    STORE the string as userString
        VARIABLE userString = INPUT

PROCESS:

Add a - between 2nd and 3rd characters
Add a ~ between 5th and 6th characters
Evaluate the string
Create a function to modify the string
    FUNCTION: formatting(userString)
        Set up loop environment
            Get length of string
            Set loop variables
                VARIABLE dash = index to place '-' (start at 2)
                VARIABLE tilde = index to place '~' ( start at 0)
            Copy user string
                VARIABLE modifiedStr = userString
        Create a loop to read and modify the string
            WHILE dash < length of userString
            Modify the string
                Add dash
                    Index into string at DASH
                    STORE as new string
                        VARIABLE new = CONCATINATE modifiedStr[:dash] + '-'
                    Edit modifiedStr
                        CONCATINATE new + modifiedStr[dash:]
                        STORE as modifiedStr
                    Set tilde index
                        tilde = dash + 6 (for correct spacing)
                Add tilde
                    Index into string at TILDE
                    STORE as new string
                        VARIABLE new = CONCATINATE modifiedStr[:tilde] + '~'
                    Edit modifiedStr
                        CONCATINATE new + modifiedStr[tilde:]
                        STORE as modifiedStr
                    Set dash index for next run
                        dash = tilde + 3 (for correct spacing)

            Return modifiedStr
    Call the function
        CALL formatting(userString)

OUTPUT:

Write the users string and modified strings to the console
    PRINT The users string is userString
    PRINT The modified string is modifiedStr
'''
#Method Header
'''Description: This method is designed to find the second and fifth places
                in a string and add the appropriate symbol then repeat

        Parameters:
            userString (str): read the string and add - or ~ based on position
            dash (int): determine the placement of the dash
            tilde (int): determine the placement of the tilde
        Return:
            modifiedStr (str): modified string with added characters
'''
# Get the users string
userString = input('Enter a random string with no spaces: ')

# Define the function
def formatting(userString) :
    # Set up loop environment
    dash = 2
    tilde = 0
    modifiedStr = userString
    # Loop through str to add characters
    while dash < len(userString):
        # Modify string
        new = modifiedStr[:dash] + '-'
        # Save changes
        modifiedStr = new + modifiedStr[dash:]
        # Count 5 places from the - for tilde index
        tilde = dash + 6
        # Modify string
        new = modifiedStr[:tilde] + '~'
        # Save changes
        modifiedStr = new + modifiedStr[tilde:]
        # Count 2 places from the ~ for dash index
        dash = tilde + 3
    return modifiedStr

# Run the function
modifiedStr = formatting(userString)

# Print statements
print(f'The original string was {userString}')
print(f'The new string is {modifiedStr}')