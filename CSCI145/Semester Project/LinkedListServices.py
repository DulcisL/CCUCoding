class Node:
    #attributes
    _data = 0
    _nextNode = None
    #constructor
    def __init__(self, data, nextNode=None):
        self._data = data
        self._nextNode = nextNode
    #GetSet
    def getData(self):
        return self._data
    def getNextNode(self):
        return self._nextNode
    def setData(self, data):
        self._data = data
    def setNextNode(self, nextNode):
        self._nextNode = nextNode

    #string
    def __str__(self):
        return f'Node Data: {self._data} NextNode: {self._nextNode}'

class LinkedList:
    #attributes
    _head = Node(0, None)
    _size = 0
    #constructor
    def __init__(self, head=None):
        self._head = head
        self._size = 0
    #getSet
    def getHead(self):
        return self._head
    def getSize(self):
        return self._size
    def setHead(self, head):
        self._head = head
    def setSize(self, size):
        self._size = size
    #behaviors
        #add Node
    def addNode(self, data):
        #construct a node
        #to be the head node
        newNode = Node(data, self._head)
        self._head = newNode
        self._size += 1
        return True
    #delete a node from the Head
    def deleteHeadNode(self):
        #Find the head node
        oldHeadNode = self._head
        #make the next node(Link) none
        nextNodeOfHead = oldHeadNode.getNextNode()
        #store the next Node(Link) as head node
        self._head = nextNodeOfHead
        #remove the nextNode(link) from the current(old) head
        oldHeadNode.setNextNode(None)
    
    #Iterate through the list
    def iterate(self, list):
        '''Description: This method is designed to iterate through the whole linked list and store in a list
        Parameters:
            list (list): Pass in the list that will store the variables

        Return:
            list (list): Nodes will be stored in the list
        '''
        current = self._head
        #loop through the nodes
        while current:
            #return the data
            list.append(current.getData())
            #Get the next node
            current = current.getNextNode()
            
        return list


        #printNode
    def printNode(self):
        #find the current head node
        current = self._head
        #loop while the current variable is not empty
        while current:
            print(current.getData())
            #store the next node into the current variable
            current = current.getNextNode()

    #str

