#working with files
#why write to files
#no database required
#the ability to save data when program has ended
#the ability to restore data when program is started

#create a text file
#create a file object variable
#open takes a file path
#R - Read
#W = Write
#O - Overwrites the file
#Ab - Appends to beginning
#Ae - Appends to end
#E - Generates errors
#mode r - RE
#mode r+ - RWAe
#mode w+ - RWAb
#mode a - WAeE
#mode w - WOAb

#+f causes an error FileNotFoundError
#catch the error and create the file if error occurred
#Import the file with the class

#exceptions - a process to control errors that may happen in your program
    #try, except
#in programming this is how you estimate and handle error to keep your program from crashing.

#ask user to enter numbers (enter any character to stop)
number = []
while True:
    try:
        userNumber = int(input('Enter a number (enter any character to stop): '))
        #save the user numbers in a list
        number.append(userNumber)
    except ValueError:
        print('You entered a character, the program ended')
        break
#Print the numbers in the list and describe each
countNumbersEntered = 1
for num in number:
    print(f'Number entered {countNumbersEntered}: {num}')
    countNumbersEntered += 1

#cause an error of an unknown exception and catch
try:
    calculation = 20/0
except ZeroDivisionError:
    print('Divide by zero error. Please try again..')
print('Program continues')

#cause a generic exception
try:
    #cal = 30/2
    #fix error
    cal = 30/2
    int(5)
#except: will work but too broad
except ZeroDivisionError:
    print('You are dividing by zero')
except ValueError:
    print('You must enter a number')
finally: # runs this block regardless
    print('Finally block executed')
print('Continue program')

#Get an items from a list at index 5 and index 7
#catch any errors