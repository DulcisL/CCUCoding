

class Sort():

    def selectionSort(self, MyList):
        for i in range(len(MyList) - 1):
            minimum = i
            for j in range(i + 1, len(MyList)):
                if (MyList[j] < MyList[minimum]):
                    minimum = j
            if (minimum != i):
                MyList[i], MyList[minimum] = MyList[minimum], MyList[i]
        return MyList

    #beg quick

    def pivot(self, array, start, end):
        # initializing
        pivot = array[start]
        low = start + 1
        high = end

        while True:

            # moving high towards left
            while low <= high and array[high] >= pivot:
                high = high - 1

            # moving low towards right
            while low <= high and array[low] <= pivot:
                low = low + 1

            # checking if low and high have crossed
            if low <= high:

                # swapping values to rearrange
                array[low], array[high] = array[high], array[low]

            else:
                # breaking out of the loop if low > high
                break

        # swapping pivot with high so that pivot is at its right # #position
        array[start], array[high] = array[high], array[start]

        # returning pivot position
        return high

    def quick_sort(self, array, start, end):
        if start >= end:
            return

        # call pivot
        p = self.pivot(array, start, end)
        # recursive call on left half
        self.quick_sort(array, start, p - 1)
        # recursive call on right half
        self.quick_sort(array, p + 1, end)

    #end quick

    def mergesort(self, x):
        if len(x) < 2:  # Return if array was reduced to size 1
            return x

        result = []  # Array in which sorted values will be inserted
        mid = int(len(x) / 2)

        y = self.mergesort(x[:mid])  # 1st half of array
        z = self.mergesort(x[mid:])  # 2nd half of array
        i = 0
        j = 0
        while i < len(y) and j < len(z):  # Stop if either half reaches its end
            if y[i] > z[j]:
                result.append(z[j])
                j += 1
            else:
                result.append(y[i])
                i += 1
        result += y[i:]  # Add left over elements
        result += z[j:]  # Add left over elements
        return result