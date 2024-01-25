import time

class Timer():
    _startTime = 0.0
    _endTime = 0.0
    _timerInstance = time

    def __init__(self):
        self._startTime = 0.0
        self._endTime = 0.0
        self._timerInstance = time

    def setStartTime(self, startTime):
        self._startTime = startTime
    def setEndTime(self, endTime):
        self._endTime = endTime

    def getStartTime(self):
        return self._startTime
    def getEndTime(self, endTime):
        return self._endTime

    def startTimer(self):
        self._startTime = self._timerInstance.time_ns()
    def stopTimer(self):
        self._endTime = self._timerInstance.time_ns()

    def results(self):
        totalTime = self._endTime - self._startTime
        print(f'{totalTime} nanoseconds')

    def resetTimer(self):
        self._startTime = 0.0
        self._endTime = 0.0