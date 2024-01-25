#Binary Search Tree
#In computer science, a binary search tree (BST), also called an ordered or sorted binary tree,
# is a rooted binary tree data structure whose internal nodes each store a key greater than all
# the keys in the node's left subtree and less than those in its right subtree

#A BST is a fast data structure that stores data in an ordered fashion
#store and search is faster than linked list and most data types.
#a node is a data object in the tree
#a node stores the data and the link (reference)
#the nodes are connected by the reference to the next node

#BST has a root - the root node is marked as head in code
#BST has a leaf(s) the leaf is determined by a null reference (next node)
    #parent
    #child
    #sibling
    #leaf
    #height of the tree
    #forests - multiple trees used together
#NOTE No duplicate data is allowed in a BST
#create a tree instance
import TreeServices
tree = TreeServices.BinarySearchTree()
tree.addNode(20)
print(f'GetRoot {tree.getRoot()}')
tree.addNode(10)
tree.addNode(25)
tree.addNode(15)
tree.addNode(9)
tree.addNode(30)
tree.addNode(22)
tree.addNode(8)
print('Traverse throught the tree')
tree.printTree()
print('Traverse In order')
tree.traverseInorder()
print('Traverse pre order')
tree.traversePreorder()