class Search():


    def linearSearch(self, searchList, length, key):
        for i in range(0, length):
            if (searchList[i] == key):
                return i
        return -1

    def binarySearch(self, searchList, low, high, key):  #user-defined function
        if high >= low:  #check base case
            mid = (high + low) // 2
            if (searchList[mid] == key):
                return mid
            elif (searchList[mid] > key):
                return self.BinarySearch(searchList, low, mid - 1, key)
            else:
                return self.BinarySearch(searchList, mid + 1, high, key)
        else:
            return -1