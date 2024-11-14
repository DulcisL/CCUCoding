War Networked Project 
Lakota Dolce
CSCI 356
Dr. Fuchs

Description:
    This project is designed to play a game of war over a user designated amount of rounds
    There can be no tie at the end of the rounds and so a sudden death round may be needed

How to run:
    To run this project you will need to use Make version XX.XXX at a minimum.
    To compile use:
        'make --build build'
    Once compiled run using:
        './build/War (#rounds)'

Known errors or bugs / needed features:
    Needs adapted from pipes to use pass over a network (localhost) rather than a pipe
    Needs sudden death round if overall rounds result in a tie
    Need to reap child methods when exiting
    Formatting is messed up when printing
    Loop off by 1
