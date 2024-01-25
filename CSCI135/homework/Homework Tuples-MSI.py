myList = []
print(myList)

myTuple = ('Go', 5.6, 12)
myList = ['Hi', 2, 4.5]
print(myList)

print('----')
print(myList[0])

print('----')
print(myList[0:2])

print('----')
print(myTuple[0])

print('----')
print(myTuple[0:2])


myList = [1,2,3]
myList[1] = 5
print(myList)
print('----')
myTuple = (1,2,3)
#myTuple[1] = 27
#print(myTuple)
#Tuples could be used to store data that you don't want changed
#by a function

L1 = [1,2,3,4]
L2 = [1,2,4,5]
T1 = (6,7,8,9)
T2 = (6,7,9,10)

if 4 in L1:
    print('yes')
if 4 in T1:
    print('yes')
if L2 > L1:
    print('List Greater')
if T2 > T1:
    print('Tuple greater')

newList = list(T1)
print(newList)
newTuple = tuple(L1)
print(newTuple)

theList = []
print(theList)
theList.append('Yo')
print(theList)
theList.remove('Yo')
print(theList)
#theList.remove('X')
#print(theList)
#You could use an if statement using the count function
#to look for the thing you want to remove.

#theList.append(4,5)
#print(theList)
#I got an error saying that it can only take one argument
# this was given because you were giving it two arguments

myList = [1,2]
myList.extend([10,11])
print(myList)
print('----')
print(myList + [14,15])

myList.insert(0,'X')
print(myList)
#It added the elements to the beginning of the list.

myList.insert(len(myList),'Q')
print(myList)


myList = [1,2,3]
#myList.pop()
print(myList)
#pop removed the last element by default

val = myList.pop(1)
print(val)
print(myList)

#myList.pop(len(myList))
#If no value is found then 0 is returned.

