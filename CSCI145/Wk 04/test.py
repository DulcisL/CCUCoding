string = input('Enter a string: ')
name = ''
try:
    if len(string) > 10:
        #change the indices to match the string
        #add a = to the middle of a string
        #convert to an int
        index = int(len(string) / 2)

        print(string[:index] + '=' + string[index + 1:])
        name = string[:index] + '=' + string[index + 1:] # will work outside the try/except block but should
                                                            # set value beforehand
    else:
        raise ValueError('SizeOfStringError')
except ValueError:
    print('Your string must be larger than 10 characters')
finally:
    print('String evaluated')
    print(name)

