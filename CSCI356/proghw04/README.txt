War Networked Project 
Lakota Dolce
CSCI 356
Dr. Fuchs

Description:
    This project is designed to play a game of war over a user designated amount of rounds
    There can be no tie at the end of the rounds and so a sudden death round may be needed

How to run:
    This project was built using make 3.82
    To compile use:
        'make'
    Once compiled run using:
        './war (#rounds)'

Known errors or bugs:
    No context given if errors occur
    No error handling if program runs out of resources
    No error handling if insufficient permissions when listening or binding
    No error handling or checking for message being passed or recieved correctly / fragmented
    Possible zombie processes children are not reaped
