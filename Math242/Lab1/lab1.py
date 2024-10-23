import numpy as np

"""
Lakota Dolce
Lab 1
"""

firstq = np.array([3,8,13,18,37,43])
print("1a: ", firstq[4])
print()

secondq = np.array([[10,20,30,40],[60,70,80,90]])
print(secondq[1][1])
print()

x = np.arange(5, 81, 1)
print("1b: ", x)
print()

y = np.arange(2.5, 100.5, .5)
print("1c: ", y)
print()

z = np.arange(100, 0, -1)
print("1d: ", z)
print()

a = np.linspace(1,1,15, dtype=int)
print("1e: ", a)

b = np.linspace(7,7,13, dtype=int)
print("1f: ", b)

identity = np.array([[1,0],
                     [0,1]])
print("1g: ", np.asmatrix(identity))
print()

zeromatrix = np.array([[0, 0, 0],
                       [0, 0, 0],
                       [0, 0, 0]])
print("1h: ", np.asmatrix(zeromatrix))
print()

print("1j: Identity: ", identity.shape)
print()

print("Zero Matrix:", zeromatrix.shape)