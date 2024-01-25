#program header
''' Name: Lakota Dolce
Date: 1/11/2023
Assignment:
Pseudocode:(when needed)
'''
# Ask for how many numbers the user wants
desires = int(input('How many numbers do you want to add? '))

# Create loop to add numbers to a list
numbers = []
runs = 0
while runs < desires:
    runs += 1
    numbers.append(int(input(f"Enter number {runs} here: ")))

'''Description: This method is designed to sum the numbers in the list
        Parameters:
            numbers (list): contains the list of numbers from the user
        Return:
            total (int): The total of that sum
'''
def sums (numbers):
    total = sum(numbers)
    return total

'''Description: This method is designed to find the smallest number in a list
        Parameters:
            numbers (list): contains the list of numbers from the user
        Return:
            smallest (int): smallest number
'''
def smallestNumber(numbers):
    # Iterate through the list
    smallest = numbers[0]
    for x in range(len(numbers)):
        #compare the list for smallest number
        if numbers[x] <= smallest:
            smallest = numbers[x]
            continue
        if numbers[x] > smallest:
            continue
    return smallest

'''Description: This method is designed to average out the numbers in the list
        Parameters:
            numbers (list): contains the list of numbers from the user
            sum (int): contains the sum of the list previously calculated
        Return:
            average (flt): The average of the numbers
'''
def averageNumber(numbers, sum):
    average = sum / len(numbers)
    return average

# Print all statements
sum = sums(numbers)
smallest = smallestNumber(numbers)
averages = averageNumber(numbers, sum)
print(f'You wanted {desires} numbers')
print(f'The sum of the numbers was {sum}')
print(f'The smallest number was {smallest}')
print(f'The average was {averages}')