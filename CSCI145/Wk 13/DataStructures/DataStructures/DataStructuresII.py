#linked list
#A linked list is a fast data structure that can store any type of data
#A linked list is unordered and has no index only links
#a node is a link in the chain
#a node stores the data and the link (reference)
#the nodes are connected by the reference to the next node
#LL has a head - the head node is marked as head in code
#LL has a tail the tail is determined by a null reference (next node)
#reference AKA next node
import LinkedListServices
ll = LinkedListServices.LinkedList()
ll.addNode(2)
ll.addNode(10)
ll.addNode(0)
ll.printNode()
print('remove the head node')
ll.deleteHeadNode()
ll.printNode()
print('create a link list with words')
#create a new link list instance
ll2 = LinkedListServices.LinkedList()
ll2.addNode('First name')
ll2.addNode('Second name')
ll2.addNode('Third name')
ll2.printNode()
print('Remove the head node')
ll2.deleteHeadNode()
ll2.printNode()
name1 = input("Please enter a name")
ll2.addNode(name1)
ll2.printNode()