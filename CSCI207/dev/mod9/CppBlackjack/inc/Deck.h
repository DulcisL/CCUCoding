/**
 * @file Deck.h
 * @author Lakota Dolce
 * @brief This is the include (header) file for a deck.
 * @version 0.1
 * @date 2024-10-08
 *
 *
 */
#pragma once //prevents recursively including file must be at the top of every .h file

#include "Card.h"

#include <string>
#include <vector>
using namespace std;

class Deck {
    private:
        // private attributes
        vector<Card> _deck;
        
        /*buildDeck
        Desc: Creates 52 individual cards by way of a nested for loop and stores it in the deck vector
        Params -> none
        Return -> none
        */
        void buildDeck(int decksNeeded, bool isFaceUp);

        /*Shuffle
        Desc: Shuffles the deck to be random
        Params -> numShuffles - number of times for the deck to be shuffled
        Returns -> none
        */
        void shuffle();

    public: 

        /** Parameterized constructor
        * @desc: Constructs a deck of the needed size
        * @param -> int numDecks - the number of decks needed to play
        * @param -> isFaceUp - a boolean value of if the cards are face up or down
        * @return -> none
        */
        Deck(int numDecks, bool isFaceUp);

        //Call the constructor
        Deck();

        /*deal
        Desc: Deals cards to the user and removes them from the vector
        Params -> none
        Returns -> card
        */
        Card Deal();

        /*sizeOf
        Desc: returns the size of the deck
        Params -> none
        Returns -> int size of deck
        */
        int SizeOf();

        /*ToString
        Desc: Used to print out the deck
        Params -> none
        Returns -> string
        */
        string ToString();

};