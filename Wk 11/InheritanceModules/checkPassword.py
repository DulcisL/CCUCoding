#program header
''' Name:
Date: 09/28/2022
Assignment: Password Check Module
Pseudocode:(when needed)
Module to check if a password contains at least 1 capital letter,1 number, and 8 characters
'''

def checkPassword(password: str):
   #8 characters
        #pass in the user password as an attribute(variable) to the method
        #count each character of the string -> len() is the method to count a string
        # check if the count is at least 8
        if len(password) >= 8:
            # 1 capital letter
            #check each character of the string and deterine if one is capital
            counter = 0
            while counter < len(password):
                #this will be a charcater in the password string
                charcterToCheck = password[counter]
                if charcterToCheck.isupper():
                    break
                counter += 1
            # 1 number
            numberCounter = 0
            while numberCounter < len(password):
                #this will be a charcater in the password string
                charcterToCheck = password[numberCounter]
                if charcterToCheck.isalnum():
                    return True
                numberCounter += 1
            return False
        else:
            return False

