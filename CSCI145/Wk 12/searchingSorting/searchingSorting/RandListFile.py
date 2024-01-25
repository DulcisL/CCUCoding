from random import seed
from random import randint

class RandList():
    _randList = []

    def __init__(self):
        self._randList = []

    def setRandList(self, randList):
        self._randList = randList

    def getRandList(self):
        return self._randList

    def createRandomList(self, amount):
        count = 0
        #number to begin the range
        seed(1)
        while count < amount:
            self._randList.append(randint(0, 2000))
            count += 1

    def showFirtTenOfList(self):
        print('First 10 of list')
        print(self._randList[:10])

    def showFirtTenOfGivenlist(self, ranList):
        print('First 10 of sorted list')
        print(ranList[:10])
    def empytList(self):
        self._randList = []
