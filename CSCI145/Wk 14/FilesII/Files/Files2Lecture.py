#Write to file
#create a text file called testDataFile and write test data and date
#create a new variable to hold the file descriptor object (file instance)
#default mode is r only to read
#modes to write r+, w, w+, a, a+
testFileInstance = open('testDataFile.txt', 'w')
testFileInstance.write('Test Data\n')
testFileInstance.write('10/21/2022')
#you must close your file to save
testFileInstance.close()

#read a file
#change the mode of the file to a mode to read r, r+ and w+
testFileInstanceRead = open('testDataFile.txt', 'r')
myDataFromTextFile = testFileInstanceRead.read()
print(myDataFromTextFile)
#close File
testFileInstanceRead.close()

#create directory
#named dirCreateFiles2
#import the os from python (allows python access files on computer)
import os
directoryToCreate = 'dirCreateFiles2'
directoryToCreateMove = 'dirCreateFilesMove'
#check if directory already exist if so skip else create
while not os.path.exists(directoryToCreate):
    os.mkdir(directoryToCreate)
while not os.path.exists(directoryToCreateMove):
    os.mkdir(directoryToCreateMove)

#move a file
#move testDataFile.txt to dir dirCreateFiles2
#source file (file you want to move)
#destination file (Were you want the file to be moved to)
#Will raise exception if file exists already
'''sourceFile = 'testDataFile.txt'
destination = 'dirCreateFiles2/testDataFile.txt'
os.rename(sourceFile, destination)

#Move to the other directory
sourceFile = 'dirCreateFiles2/testDataFile.txt'
destination = 'dirCreateFilesMove/testDataFile.txt'
os.rename(sourceFile, destination)

#Note will raise exception if file doesn't exist beforehand
fileToRemove = 'myData.txt'
#delete a file
os.remove(fileToRemove)
'''

#Save an object to a file to store
import pickle
import CarService

carClassFile = 'CarData.txt'
carFileObject = open(carClassFile, 'wb')
myNewCar = CarService.Car()
myNewCar.setName('Mustang GT')
#Store in the file
pickle.dump(myNewCar, carFileObject)

#Restore the car object and all data from the text file
#destroy car object in memory
del myNewCar

carFileObject.close()
#Restore
#create a file descriptor object in read mode
carFileInRead = open(carClassFile, 'rb')
myNewCar = pickle.load(carFileInRead)

print(myNewCar)

carFileInRead.close()