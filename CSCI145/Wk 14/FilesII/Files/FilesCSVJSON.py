#CSV File - Comma Seporated Value
#text table format
#file rows are equal to table rows

#example
#ClassName, ClassNumber, ClassRoom
#Intermediate Programming, CSCI 145, AOC2 240
#Into to Multimedia Apps, CSCI 375, AOC2 217
#Human Computer Interaction, CSCI 444, Online
#Software Engineering II, CSCI 490, AOC2 240
#Fundamentails of Data-Driven Programming, IST 600, Online

    #create a CSV File
myCSVFile = open('classList.csv', 'w')
myCSVFile.write('ClassName, ClassNumber, ClassRoom\n')
myCSVFile.write('Intermediate Programming, CSCI 145, AOC2 240\n')
myCSVFile.write('Into to Multimedia Apps, CSCI 375, AOC2 217\n')
myCSVFile.write('Human Computer Interaction, CSCI 444, Online\n')
myCSVFile.write('Software Engineering II, CSCI 490, AOC2 240\n')
myCSVFile.write('Fundamentails of Data-Driven Programming, IST 600, Online\n')
myCSVFile.close()
#JSON File

    #create a JSON file
import json
myJSONFile = open('testJSONData.json', 'w')
myJSONFile.write('{ "fruit": "Apple", "size": "Large", "color": "Red"}')
myJSONFile.close()

jsonString = '{ "fruit": "Apple", "size": "Large", "color": "Red"}'
jsonObject = json.loads(jsonString)
print(jsonObject['size'])
#convert JSON string to a python object.