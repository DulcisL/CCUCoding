myList = []
name = input('Enter a Name: ')
while name != '':
    myList.append(name)
    name = input('Enter a name:')
print('\nName List:')
count = 0
i = 0
while i < len(myList):
    print(myList[i])
    if len(myList[i]) > 12:
        count += 1
    i += 1
print('\n', count, 'Long Names')

letters = ['a', 'b', 'c',]
numbers = [1, 2, 3]
i = 0
while i < len(letters):
    j = 0
    while j < len(numbers):
        print('%s%d' % (letters[i], numbers[j]))
        j+= 1
        i += 1
print('Done')
# 1) The loop will never run.

# 2) You could use it but it may not work as well as a sentinel variable compared to something that is specifically for it

# 3) It would prevent J from resetting to run the nested loop whenever a new list was made.

