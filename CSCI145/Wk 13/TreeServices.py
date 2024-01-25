#node Class
class Node:
    _data = None
    _left = None
    _right = None

    def __init__(self, data=None, left=None, right=None):
        self._data = data
        self._left = left
        self._right = right

    def getData(self):
        return self._data
    def getLeft(self):
        return self._left
    def getRight(self):
        return self._right

    def setData(self, data):
        self._data = data
    def setRight(self, right):
        self._right = right
    def setLeft(self, left):
        self._left = left
    def traversePreorder(self):
        print(self._data)
        if self._left:
            self._left.traversePreorder()
        if self._right:
            self._right.traversePreorder()

    def traverseInorder(self):
        if self._left:
            self._left.traverseInorder()
        print(self._data)
        if self._right:
            self._right.traverseInorder()

    def traversePostorder(self):
        if self._left:
            self._left.traversePostorder()
        if self._right:
            self._right.traversePostorder()
        print(self._data)

    def search(self, target):
        if self._data == target:
            print("Found it!")
            return self

        if self._left and self._data > target:
            return self._left.search(target)

        if self._right and self._data < target:
            return self._right.search(target)

        print("Value is not in tree")

    def getNodesAtDepth(self, depth, nodes=[]):
        if depth == 0:
            nodes.append(self._data)
            return nodes

        if self._left:
            self._left.getNodesAtDepth(depth - 1, nodes)
        else:
            nodes.extend([None] * 2 ** (depth - 1))

        if self._right:
            self._right.getNodesAtDepth(depth - 1, nodes)
        else:
            nodes.extend([None] * 2 ** (depth - 1))
        return nodes

    def insertNode(self, newData):
        # Do nothing if no data
        if self._data:
            # Where data value is less than current, branch left
            if newData < self._data:
                if self._left is None:
                    self._left = Node(newData)
                else:
                    self._left.insertNode(newData)
            # Where data is greater than current, branch right
            elif newData > self._data:
                if self._right is None:
                    self._right = Node(newData)
                else:
                    self._right.insertNode(newData)

    def height(self, h=0):
        leftHeight = self._left.height(h + 1) if self._left else h
        rightHeight = self._right.height(h + 1) if self._right else h
        return max(leftHeight, rightHeight)

    def __str__(self):
        return f'Node Data: {self._data} Left Value: {self._left} Right Value: {self._right}'

#BinarySearchTree Class
class BinarySearchTree:
    _root = Node
    _name = str

    def __init__(self, root=Node()):
        self._root = root
        self._name = "Family Tree"

    def getRoot(self):
        return self._root
    def getStr(self):
        return self._str

    def setRoot(self, root):
        self._root = root
    def setStr(self, str):
        self._str  = str

    def addNode(self, value):
        if self._root.getData() is None:
            self._root = Node(value)
        else:
            self._root.insertNode(value)
                # if data > par.getData():
                #     print('Adding in right of ', par.getData(), 'new node ', data)
                #     par.setRight(node)
                # else:
                #     print('Adding in left of ', par.getData(), 'new node ', data)
                #     par.setLeft(node)



    #traverse through tree (used to print or find a node)
    def _nodeToChar(self, n, spacing):
        if n is None:
            return '_' + (' ' * spacing)
        spacing = spacing - len(str(n)) + 1
        return str(n) + (' ' * spacing)

    def printTree(self, label=''):
        print(self._name + ' ' + label)
        height = self._root.height()
        spacing = 3
        width = int((2 ** height - 1) * (spacing + 1) + 1)
        # Root offset
        offset = int((width - 1) / 2)
        for depth in range(0, height + 1):
            if depth > 0:
                # print directional lines
                print(' ' * (offset + 1) + (' ' * (spacing + 2)).join(
                    ['/' + (' ' * (spacing - 2)) + '\\'] * (2 ** (depth - 1))))
            row = self._root.getNodesAtDepth(depth, [])
            print((' ' * offset) + ''.join([self._nodeToChar(n, spacing) for n in row]))
            spacing = offset + 1
            offset = int(offset / 2) - 1
        print('')

    #delete a node from the tree
    def deleteNode(self, node: Node):
        print("Create this method to use")

    def traverseInorder(self):
        self._root.traverseInorder()

    def traversePreorder(self):
        self._root.traversePreorder()

    def traversePostorder(self):
        self._root.traversePostorder()

    def search(self, target):
        return self._root.search(target)

    def getNodesAtDepth(self, depth):
        return self._root.getNodesAtDepth(depth)

    def height(self):
        return self._root.height()
