def ascendingSelectionSort(MyList):
    for i in range(len(MyList) - 1):
        minimum = i
        for j in range( i + 1, len(MyList)):
            if(MyList[j] < MyList[minimum]):
                minimum = j
        if(minimum != i):
            MyList[i], List[minimum] = MyList[minimum], MyList[i]
    return MyList