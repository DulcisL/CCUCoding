# Queues are also a very fundamental and important concept to grasp since many other data structures
# are built on them.
# The way a queue works is that the first person to join the queue usually gets served first,
# all things being equal. The acronym FIFO best explains this. FIFO stands for first in, first out.
# When people are standing in a queue waiting for their turn to be served,
# service is only rendered at the front of the queue. The only time people exit the queue is
# when they have been served, which only occurs at the very front of the queue.

#create a list to use as a queue
queue = []

#add items to the queue
queue.append('A')
queue.append('B')
queue.append('C')
queue.append('D')

#print the raw queue
print('Raw Queue (do not use in a finished program)')
print(queue)

#print the queue for the console described
print('Queue described')

def printQueueDescribed():
    count = 0
    for item in queue:
        print(f'{count} - {item}')
        count += 1
printQueueDescribed()
#remove an item from the queue
#you can only remove an item at index 0
#if you remove using another index you are not using a queue
print('Remove an item from the queue (A)')
queue.pop(0)

print('Queue with an item removed')
printQueueDescribed()


#What data structure would be best to use?

#an undo function in a program - Stack
#who arrived first - Queue
#who would move first on a green light - Queue
#deconstruct a tower - Stack
#chop down a treen - Stack
