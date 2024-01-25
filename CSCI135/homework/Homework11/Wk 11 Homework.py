import csv
f=open('data.csv')
reader = csv.reader(f,delimiter=',')
for row in reader:
    print(row)