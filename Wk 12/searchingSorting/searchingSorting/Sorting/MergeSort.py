def mergesort(x):
    if len(x) < 2:  # Return if array was reduced to size 1
        return x

    result = []  # Array in which sorted values will be inserted
    mid = int(len(x) / 2)

    y = mergesort(x[:mid])  # 1st half of array
    z = mergesort(x[mid:])  # 2nd half of array
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

