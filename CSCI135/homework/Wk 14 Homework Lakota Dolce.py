import numpy as np

a = [1, 2, 3, 4]
x = np.array(a)
print(type(a))
print(type(x))
print(a)
print('----')
print(x)

x = np.zeros((4))
print(x)
y= np.full((2,2),27)
print(y)
z=y

print(z)
z[1][0]=34
print(y)

print(y)
y=y*10 # multiply every element in array by 10
print('---')
print(y)
z=y+y # add two arrays together
print('--')
print(z)

print(y)
print('---')
print(y.shape)
y.reshape((4))
print('---')
print(y)