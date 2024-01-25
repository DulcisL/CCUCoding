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

#load file to use class and methods
import FileServices
fs = FileServices.FileServices()
#create a Directory
fs.createDir()


data = 'This is my first text file\nThis is the second line of my first text file'
fs.setData(data)
fs.setFileName('myData.txt')
fs.setMode('a')
fs.writeToFile()
print(fs)
fs.setData(fs)
fs.writeToFile()
fs.setData("line 2 of data")
fs.writeToFile()
fs.setData("line 3 of data")
fs.writeToFile()
fs.setData("line 4 of data")
fs.writeToFile()
print('Data from file')
fs.setMode('r')
fs.readFromFile()
print('Data from file using read lines')
myListFromFile = fs.readLinesFromFile()
print("This is the 5th line from the text document")
print(myListFromFile[4])



#open file again
# myTextFile = open('myData.txt', 'a')
# myTextFile.write('This will append to the top of the file\n')
# myTextFile.write('---------------------------------------\n')
#close file again
# myTextFile.close()

#change modes to write to file
myTextFile = open('myData.txt', 'r')
lines = myTextFile.readlines()
countLine = 1
for line in lines:
    print(f'{countLine} -> {line}')
    countLine += 1
myTextFile.close()

#where is my file
findFile = open('myData.txt', 'a')
print(findFile.tell())
findFile.close()

#find data in a location in a file
locateData = open('myData.txt', 'r')
#first argument is position, second argument is option
#options
#0 - absolute value
#1 - relative to current position
#2 - Relative to the end
# print(locateData.seek(12, 0))
# findDataAtlocation = locateData.readlines()
# print(f'Data at location 2 {findDataAtlocation[locateData.seek(2,0)]}')

#+f causes an error FileNotFoundError
#catch the error and create the file if error occured
#Import the file with the class
