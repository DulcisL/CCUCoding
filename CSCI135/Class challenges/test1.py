length = 0
str = []
while length < 5:
    str.append(input("Input string here: "))
    length += 1
if length == 5:
    for x in str:
        print (x)

list = []
for i in range(5):
    list.append(input("Input string here: "))
for x in list:
    print(x)