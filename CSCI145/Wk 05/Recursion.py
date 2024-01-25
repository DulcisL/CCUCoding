#Recursion is particularly useful for divide and conquer problems; however,
#it can be difficult to understand exactly what is happening,
#since each recursive call is itself spinning off other recursive calls.
#At the core of a recursive function are two types of cases:
#base cases, which tell the recursion when to terminate.
#recursive cases that call the function they are in
#recursion leads to a more natural and elegant solution

#used in trees as previous lecture.
#used in many math problems as factoring
#will be used when evaluating algorithms and estimating speed or cost.

#depth is the amount of iterations to reach the base case.

#will run until base case is met.
#If base case is never met a recursion depth exceeded while calling
# a Python object error is generated

#demo last code from slides (improper recursive case)
def fexample(number):
    if number == 1:
        return 1
    else:
        return fexample(number + 1)
#call the recursive function
# print(fexample(5))

#write a recersive method to reverse a string

#test negative indices
myString = 'February'
#print(myString[-1])
#print(myString[0])
#print(myString[-8])

def reverseString(myString):
    #base case
    if myString == '':
        return myString
    #recursive case
    #manipulate the string one at a time
    print("--Call--")
    print(f'Current String {myString}')
    print(f'Without first character -> {myString[:-1]}')
    print(f'Only first character {myString[-1]}')
    print(f'Recursively call the rest of the string -> {myString[:-1]} -- add first {myString[-1]}')
    print('--EndCall--')
    modString = myString[1:] + myString[0]
    #print(modString)
    return myString[-1] + reverseString(myString[:-1])
#print(reverseString(myString))


#The factorial of 4 is 4 × 3 × 2 × 1 and the factorial of 5 is 5 × 4 × 3 × 2 × 1.
#Say that 5! = 5 × 4!.
def factorial (number):
    #base case - number entered must eventually reach 1
    #for the number to reach 1 must decrease by 1
    if number == 1:
        return number
    #recursive call - Will decrease the number entered by 1 until base case
    #number -1
    # how to detemine a factorial
   #as the number decreases must multipy by the number
    #The order of operations matters
    # perform the math before the recursive call, if each number needs to be multiplied
    #write the math after if the math is to happen when function is complete
    return number * factorial(number - 1)
#print(factorial(10))



#This is recursive because the definition of the factorial of 5 (or any number n)
# includes the definition of the factorial of 4 (the number n – 1).
#In turn, 4! = 4 × 3!, and so on, until you must calculate 1!, the base case, which is simply 1.

#define a function that reads the characters in a word one by one from left to right
# and prints them vertically None with the base_case point at the end of the word.

def verticalStr(word):
    #base case - when the string is empty
    if word == '':
        word = 'None'
        return word
    #recursive case
    #take off the first character
    # slice string and remove one at a time
    #print the first letter
    print(word[0])
    return verticalStr(word[1:])
#print(verticalStr('Yesterday'))

#find all even numbers to a given number
# 10 all even numbers => 10, 8, 6, 4, 2
def even(number, base = 2):
    #base case - if number = 2 stop
    if base >= number:
        return number
    #recursive case
    # to reach base case subtract 2
    # must print before to show numbers
    print(base)
    return even(number,base + 2)
print(even(10))