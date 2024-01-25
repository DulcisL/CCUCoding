#program header
''' Name: Lakota Dolce
Date: 1/11/2023
Assignment:
Pseudocode:(when needed)
'''
#What is a variable
    #Named container or data type
    #name the storage container for the data it will contain

#Data types
    #int - number (short for integer)
    #float - decimal or fractional value
    #string - group of characters that represent a word or phrase
    #boolean - true / false (1 / 0)
    #char - on single letter

#variable naming convention (variable name rules)
     #No special characters
     #common naming theme for your program
     #Cannot start with a number
     #underscore to separate words
     #constants are in all caps
     #multiple names are camel-cased.
     #potatoSaladAndCole

#structure of programming
      #variables first
      #methods after variables
      #code body
      #prints

#integer
myNumber = 14
print(f"my number is {myNumber}")

#float
myDecimal = 14.5
print(myDecimal)

#string
myString = 'This is my String'
print(myString)

#string methods
print(f"Upper string {myString.upper()}")
print(f"Lower string {myString.lower()}")

#Index string
print(f'Print the 3 character of the string {myString[2]}')

#list
#integer list
myList = [1,2,3,4,5]
print(myList)

#Add to list
myList.append(28)

#Remove from list
myList.remove(3)

#print list
print(myList)

#String List
myListWords = ['One','Two','Three','Four','Five']
print(myListWords)

#add to list
myListWords.append('Twenty')

#remove from list
myListWords.remove('Three')

#print list
print(myListWords)

#print size
print(len(myListWords))

#find last item in a list
print(myListWords[len(myListWords) - 1])

#dictionary
#create a dictionary
myDict = {'name': 'Bob', 'age':15, 'name2': 'Sarah', 'age2': 15}
print(myDict['name'])
print(myDict['name2'])

#shopping information
#store data in variables
#variable name set it equal to the data type that will be stored.
# = is an assignment operator.

#ask the user to enter numbers and enter a q to stop entering numbers