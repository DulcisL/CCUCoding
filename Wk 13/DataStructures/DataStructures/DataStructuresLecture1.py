#create a stack
#stack is a data structure LIFO format
#Last in First Out

#initalize an empty list in python
myStack = []

print('How many items in stack')
print(len(myStack))

#add data to the stack bottom up.
myStack.append('A')
myStack.append('B')
myStack.append('C')
myStack.append('D')

#print the raw stack to see location
print(myStack)

#print stack in a stacked form to the console
def printStack(myStack):
    count = 1
    for items in myStack:
        print(f'{count} - {items}')
        count += 1

#call my print stack method
printStack(myStack)

#remove an item from a stack
#use the method pop
print('-remove an item from stack (LIFO)- this should remove D')
#This will remove the last item entered
myPopedItem = myStack.pop()
printStack(myStack)
print('Value removed from stack')
print(myPopedItem)

#look at the data in the stack
#use the method peek()
#python uses slice to operate the peek of a stack
print('Peek at last item in list')
print(myStack[-1:])
print(myStack[-2:])

#check if the stack has any values
print('How many items in stack')
print(len(myStack))

