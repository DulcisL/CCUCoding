my_list=[0, 1, 2, 3, 4]

for i, x in enumerate(my_list.copy()):
 my_list[i]=10+x
 print(x,'-->',my_list[i])
print(my_list)