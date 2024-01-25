#program header
''' Name: Lakota Dolce
Date: 1/11/2023
Assignment:
Pseudocode:(when needed)
'''

#asking for the user input
number = int(input('Pick a number between 1 and 10, Enter it here: '))

'''Description: This method is designed to compare the number between 1 and 10
        Parameters:
            number (int): Compare whether you like high or low numbers
        Return:
            low/high (str): You like low/high numbers
'''
def comparing (number):
    #comparing the number
    if number > 0 and number <= 5:
        low = 'You like low numbers'
        return low

    if number > 5 and number <= 10:
        high = 'You like high numbers'
        return high

compared = comparing(number)
print(f'Your number was {number}')
print(compared)