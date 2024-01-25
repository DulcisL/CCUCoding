def BinarySearch(arr, low, high, key):  #user-defined function
    if high >= low:  #check base case
        mid = (high + low) // 2
        if (arr[mid] == key):
            return mid
        elif (arr[mid] > key):
            return BinarySearch(arr, low, mid - 1, key)
        else:
            return BinarySearch(arr, mid + 1, high, key)
    else:
        return -1