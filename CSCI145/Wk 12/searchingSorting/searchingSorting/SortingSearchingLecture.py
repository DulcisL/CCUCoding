from TimerFile import Timer
from RandListFile import RandList
from SortFile import Sort
from SearchesFile import Search

#instances of classes
timerInst = Timer()
sortInst = Sort()
searchInst = Search()
randomInst = RandList()

#sort
#selection sort
randomInst.createRandomList(100)
selectionSortList = randomInst.getRandList()
randomInst.showFirtTenOfList()
timerInst.startTimer()
sortList = sortInst.selectionSort(selectionSortList)
randomInst.showFirtTenOfGivenlist(sortList)
timerInst.stopTimer()
timerInst.results()
timerInst.resetTimer()

#quick sort
#Merge Sort

#linear search

#search
#binary search

#Linear search

#Big O
