class Car ():
    _name = str

    def __init__ (self):
        self._name = 'No name'

    def setName (self, name: str):
        self._name = name

    def getName (self):
        return self._name

    def driveCar(self):
        print ('car drove 1 mile.')

    def __str__(self):
        return f'The car is named {self._name}'