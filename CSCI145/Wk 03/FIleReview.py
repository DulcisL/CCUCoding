# Create a .txt file
# Write data from the user into the text file
# Ask the user for a sentence and place the sentence in 3 lines

# Allow user to name file
# Allow user to change mode
# Handle all errors

# Ask the user for a sentence and
userString = input('Please enter a sentence ')
# Ask the user for file name
fileName = input('Enter a file name without the extension: ')
# Ask user for mode
fileMode = input('Enter a mode for your file (To write: w or a, and to read: r or r+)')
completeFile = fileName + '.txt'
# Place the sentence in 3 lines
# Into the text file
try:
    fileObject = open(completeFile, fileMode.lower())

    fileObject.write(f'User string Line 1: {userString[:9]}\n')
    fileObject.write(f'User string Line 2: {userString[9:14]}\n')
    fileObject.write(f'User string Line 3: {userString[14:]}\n')

except FileNotFoundError:
    # create the file that does not exist
    fileObject = open(completeFile, 'w')
    print('File created')
finally:
    # Save the data with close
    fileObject.close()