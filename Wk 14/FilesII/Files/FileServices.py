import os
class FileServices():
    #variables (attributes)
    _mode = ''
    _data = ''
    _fileName = ''
    _filePath = ''
    _myTextFile = None
    #Constructor
    def __init__(self):
        self._mode = 'w'
        self._data = 'Test Data'
        self._fileName = 'thisTestFile.txt'
        self._filePath = 'docs/files/'
        self._myTextFile = None
    #set (Mutator)
    def setMode(self, mode):
        self._mode = mode
    def setData(self, data):
        self._data = data
    def setFileName(self, fileName):
        self._fileName = fileName
    #get (Accessory)
    def getMode(self):
        return self._mode
    def getData(self):
        return self._data
    def getFileName(self):
        return self._fileName
    #Behaviors
    #errors thrown by writing to a file
    #io.UnsupportedOperation
    #TypeError
    #ValueError
    #FileNotFoundError
    def writeToFile(self):
        #local scope to method
        try:
            #local scope to try
            self._myTextFile = open(self._fileName, self._mode)
            # write data to the text file after open is completed
            self._myTextFile.write(f'{self._data}\n')
            # close
            # close will end the programs connection to the file
            # will save the data in the text file.
            # will cause the file to be unusable and may corrupt the file
            # completes the file
        except TypeError:
            print(f'Check your mode for correct data type for mode: {self._mode}, must be a string.')
        except ValueError:
            print(f'Check your mode you entered and invalid mode: {self._mode}.')
        except FileNotFoundError:
            print('You file does not exist.')
        except:
            print('Error: check your mode and data entered. Mode is string, Data is string')
        finally:
            self._closeFile()

    def readFromFile(self):
        #open file in a mode to read
        self._myTextFile = open(self._fileName, self._mode)
        content = self._myTextFile.read()
        print(content)
        self._closeFile()

    def readLinesFromFile(self):
        #open file in a mode to read
        self._myTextFile = open(self._fileName, self._mode)
        contentList = self._myTextFile.readlines()

        for line in contentList:
            print(line)

        self._closeFile()
        return contentList

    def createDir(self):
        newDirectory = 'MyNewDir'
        while not os.path.exists(newDirectory):
            os.mkdir(newDirectory)

    #to create a file and keep open to write multiple times in your program
    def createFile(self):
        pass

    def moveFileOrDirectory(self):
        pass

    def deleteFileOrDirectory(self):
        pass

    #a private method that can only be used in this class
    #this is call a helper method
    def _closeFile(self):
        self._myTextFile.close()

    #str method
    def __str__(self):
        return f'Mode: {self._mode} Data: {self._data} FileName: {self._fileName} Path: {self._filePath}'
