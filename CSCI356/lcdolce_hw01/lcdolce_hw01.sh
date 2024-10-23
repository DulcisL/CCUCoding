#!/bin/bash

#---------------------------------------------#                                 
#lakotadHw01.txt - Shell script for homework 1                                  
#                                                                               
#Name: Lakota Dolce                                                             
#Assignment: Homework 1                                                         
#Email: lcdolce@coastal.edu                                                     
#Date: 9/17/2024                                                                
#---------------------------------------------#                                 
                                                                                
#Make the temp directory in the home folder                                      
echo "Making the temp directory in the home folder"                             
mkdir ~/temp                                                                    
ls -a ~/                                                                        
                                                                                
#Write to the file an explanation of the df command to tem/5.out                
echo "df is a command used to see the size of a file or files that are on a driv
this can be used to see a single file or a whole drives space used of mounted drives only."            
                                                                                
#Execute df and append output to temp/5.out
df -h |tee ~/temp/5.out
echo "-----------------------------------------"|tee -a ~/temp/5.out

#Print all usernames with the first letter of your first name from passwd.txt and output to tem/6.out
grep '^l' ~/passwd.txt |tee -a ~/temp/6.out
echo "-----------------------------------------"|tee -a ~/temp/6.out

#Get the count of the users with the same starting letter as your last name
grep '^d' ~/passwd.txt |wc -l |tee -a  ~/temp/7.out
echo "-----------------------------------------"|tee -a ~/temp/7.out

#use env to print current shell environment variables and sort them alphabetically to 8.out
env | sort -d | tee ~/temp/8.out
echo "-----------------------------------------"|tee -a ~/temp/8.out

#Create a program that converts a user input number (mph) to km/h
#Show both mph and km/h and and a descriptive message repeat for Celcius and fahrenheit

#Get user input
echo "Enter a number to be converted:\n"
read number

#Convert to km/h
kmh=$(echo "scale=2; $number * 1.6" | bc)
echo "This is the number in KM/h: $kmh KM/h"|tee -a ~/temp/9.out
echo "This is the number in Mph: $number MPH"|tee -a ~/temp/9.out

#Convert to fahrenheit
fahrenheit=$(echo "$number * 9/5 + 32" | bc)
echo "This is the number in Fahrenheit: $fahrenheit F"|tee -a ~/temp/9.out
echo "This is the number in Celcius: $number C"|tee -a ~/temp/9.out
echo "-----------------------------------------"|tee -a ~/temp/9.out


#concatinate .out files into a single file called lcdolce_hw01.txt
echo "Lakota Dolce lcdolce" |tee ~/lcdolce_hw01.txt
cat ~/temp/5.out ~/temp/6.out ~/temp/7.out ~/temp/8.out ~/temp/9.out |tee -a ~/lcdolce_hw01.txt
#!/bin/bash
#Lakota Dolce lcdolce
#---------------------------------------------#                                 
#lakotadHw01.txt - Shell script for homework 1                                  
#                                                                               
#Name: Lakota Dolce                                                             
#Assignment: Homework 1                                                         
#Email: lcdolce@coastal.edu                                                     
#Date: 9/17/2024                                                                
#---------------------------------------------#                                 
                                                                                
#Make the temp directory in the home folder                                      
echo "Making the temp directory in the home folder"                             
mkdir ~/temp                                                                    
ls -a ~/                                                                        
                                                                                
#Write to the file an explanation of the df command to tem/5.out                
echo "df is a command used to see the size of a file or files that are on a driv
this can be used to see a single file or a whole drives space used of mounted drives only."            
                                                                                
#Execute df and append output to temp/5.out
df -h |tee ~/temp/5.out
echo "-----------------------------------------"|tee -a ~/temp/5.out

#Print all usernames with the first letter of your first name from passwd.txt and output to tem/6.out
grep '^l' ~/passwd.txt |tee -a ~/temp/6.out
echo "-----------------------------------------"|tee -a ~/temp/6.out

#Get the count of the users with the same starting letter as your last name
grep '^d' ~/passwd.txt |wc -l |tee -a  ~/temp/7.out
echo "-----------------------------------------"|tee -a ~/temp/7.out

#use env to print current shell environment variables and sort them alphabetically to 8.out
env | sort -d | tee ~/temp/8.out
echo "-----------------------------------------"|tee -a ~/temp/8.out
rm ~/temp/10.out

#Create a program that converts a user input number (mph) to km/h
#Show both mph and km/h and and a descriptive message repeat for Celcius and fahrenheit

#Get user input
echo "Enter a number to be converted:\n"
read number

#Convert to km/h
kmh=$(echo "scale=2; $number * 1.6" | bc)
echo "This is the number in KM/h: $kmh KM/h"|tee -a ~/temp/9.out
echo "This is the number in Mph: $number MPH"|tee -a ~/temp/9.out

#Convert to fahrenheit
fahrenheit=$(echo "$number * 9/5 + 32" | bc)
echo "This is the number in Fahrenheit: $fahrenheit F"|tee -a ~/temp/9.out
echo "This is the number in Celcius: $number C"|tee -a ~/temp/9.out
echo "-----------------------------------------"|tee -a ~/temp/9.out


#concatinate .out files into a single file called lcdolce_hw01.txt
cat ~/temp/5.out ~/temp/6.out ~/temp/7.out ~/temp/8.out ~/temp/9.out |tee ~/lcdolce_hw01.txt
