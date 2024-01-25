#modules
#https://docs.python.org/3/py-modindex.html
#python Docs
#https://docs.python.org/3
import calendar as cs
import libraryFile
import onlineLibFile
#use the library imported by typing library
#use the dot to call the Library class to create an instance
print(cs.TextCalendar)
#lib is the instance variable
#library is the module
#Library is the class
lib = libraryFile.Library('module Lib', 100, 'The Mod worker name')
print(lib)
subLib = onlineLibFile.OnlineLib('mobLib.com', 'online', 2000, 'you', True)
print(subLib)
#create a module for the library class

#test the module for checking is a password is valid
#import module to use the passwordChecker
import checkPassword
password = input('Enter a paSsword \n (must have 1 capital letter, 1 number and 8 characters): ')
if checkPassword.checkPassword(password):
    print(f'password {password} is accepted')
else:
    print('password not accepted')

#classes and methods in separate files
#Multiple inheritances
#private Methods
# Polymorphism
    # Polymorphism in python defines methods in the child class that have the same name as the
    # methods in the parent class. In inheritance, the child class inherits the methods from the
    # parent class. Also, it is possible to modify a method in a child class that it has inherited
    # from the parent class.
# duck typing
    # Duck typing is a concept related to dynamic typing, where the type or the class of an
    # object is less important than the methods it defines. When you use duck typing, you do not
    # check types at all. Instead, you check for the presence of a given method or attribute
