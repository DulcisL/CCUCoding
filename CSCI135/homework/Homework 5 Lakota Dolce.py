from re import M


one = "String 1"
print(len(one))
two = ''
print(len(two))
print(one[1])
print(one[5])

my_str = "Monty Python"
print(my_str[-10])
print(my_str[-4])
print(my_str[0:4])

print(my_str[-13:-6])
print(my_str[-6:-1])
print(my_str[-1:-6])

print(my_str[-6:])
print(my_str[:5])
print(my_str[:])

print(my_str[-13:-6:2])
print(my_str[::2])

print(my_str[4:0:-1])

print(my_str)
#my_str[8] = 'Q'
new_str = my_str + 'X' + my_str
print(new_str)

x = 'This is a test'
y = x.split()
print(y)
print(x)

x = 'A lot of         Spaces'
print(x.split())

y = 'Hello Python'
print(y.split(','))

sep = ':'
x = sep.join(['a','b'])
print(x)

a = 'X'
b = 'x'
c = ';'
print(a.islower())
print(b.islower())
print(c.islower())

print(a.upper())
print(b.upper())
print(c.upper())

print(y.find('o'))
print(y.find('on'))
print(y.find('g'))

print(y)
print(y.find('o',7))

print(y)
print(y.find('on',7,12))

print(y)
print(y.find('ell',1))
print(y.find('ell',2))

print(y)
print(y.lower().replace('o','X'))

print(y.lower().replace('o','X').split(','))
#print(y.lower().split(',').replace('o','X'))