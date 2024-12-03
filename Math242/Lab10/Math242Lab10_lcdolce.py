"""
Lakota Dolce
Math 242
Lab 10
Dr. Debendra
"""

import numpy as np
from fractions import Fraction

"""Find smallest
desc: Finds the smallest nonzero number in an array
param:array - takes an array of numbers
return: float - returns a floating point number that is nonzero
"""
def findSmallest(array):
    #Find smallest
    smallest = 1
    size = array.size
    for i in range(size):
        try:
            if array[i] < array[i+1]:
                if array[i] != 0:
                    smallest = array[i]
                continue
            else:
                if array[i+1] != 0:
                    smallest = array[i+1]
                continue
        except:
            continue
    return smallest

#Initialize
values = []
count = 1
string = ""

#Define the matrix
matrixA = np.array([[-1,4], [0,3]])
matrixB = np.array([[2,7], [-1,-6]])
matrixC = np.array([[-1,0,0], [1,2,0], [2,-2,3]])

#Calculate Eigen Values / Vectors
eigenValA , eigenVecA = np.linalg.eig(matrixA)
eigenValB , eigenVecB = np.linalg.eig(matrixB)
eigenValC , eigenVecC = np.linalg.eig(matrixC)

#Print the values, vectors
print(eigenValA, eigenVecA)
print()
print(eigenValB, eigenVecB)
print()
print(eigenValC, eigenVecC)
print()

#Get smallest nonzero number in array
smallestA = findSmallest(eigenVecA)
smallestB = findSmallest(eigenVecB)
smallestC = findSmallest(eigenVecC)

#Make readable by dividing by the smallest non-zero number
#Print it out
#Get the eigen val
for i in range(eigenValA.size):
    #Get the corresponding vector values
    for j in range(values / eigenValA.size):
        #print
        print(f"Eigen Pair (a-{count}) ({int(eigenValA[i])}, ({values[j]})")
        count += 1
values = []
count = 0

