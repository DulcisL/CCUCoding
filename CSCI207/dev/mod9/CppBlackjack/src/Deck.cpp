/**
 * @file Deck.cpp
 * @author Lakota Dolce
 * @brief This is the definition (source) file for a deck
 * @version 0.1
 * @date 2024-10-08
 *
 */
#include "Deck.h"
#include "Card.h"

#include <vector>
#include <string.h>
#include <stdexcept>
#include <iostream>

/**
 * @brief Parameterized Construct a new Deck
 *
 * @param None
 */
Deck::Deck (){
    //Create the deck 
    buildDeck();
}

/*buildDeck
Desc: Creates 52 individual cards by way of a nested for loop and stores it in the deck vector
Params -> deck (Vector) - contains the array to be used to store the deck (passed by reference)
Return -> none
*/
void Deck::buildDeck(){
    //run 13 times to make card
    for (int i = 1; i < 14; i ++){
        //run 4 times to get suits
        for (int j = 1; j < 5; j++){
            //make the card
            Card card = Card(i,j,true);
            //push the card to the vector
            _deck.push_back(card);
        }
    }
    //Shuffle the deck
    Shuffle();
}

/*Shuffle
Desc: Shuffles the deck to be random
Params -> deck (vector) - Store the deck to be shuffled (passed by reference)
          numShuffles - number of times for the deck to be shuffled
Returns -> none
*/
void Deck::Shuffle(){
    //Initialize
    int numShuffles = 1000;
    //seed the rand
    srand(time(NULL));

    //set up loop
    int indice1;
    int indice2;
    int i = 0;
    while (i < numShuffles){

        //get indices use modulo to keep within deck size
        indice1 = i % _deck.size();
        indice2 = rand() % _deck.size();

        //swap places
        swap(_deck[indice1], _deck[indice2]);
        i++;
    }   
}

/*deal
Desc: Deals cards to the user and removes them from the vector
Params -> Vector<Card> deck - Contains the deck of cards (passed by reference)
          int numCards - The number of cards to be dealt
Returns -> none
*/
Card Deck::deal(){
    //Check if deck is empty
    if (!_deck.empty()){
        //Inform player
        cout << "Dealing cards... \n";

        //Get the card at the beginning
        Card card = _deck.back();

        //erase the card at the beginning
        _deck.pop_back();

        //return the card
        return card;
    }
    else {
        throw std::out_of_range("No cards in deck");
    }
}

/*sizeOf
Desc: returns the size of the deck
Params -> none
Returns -> int size of deck
*/
int Deck::sizeOf(){
    return _deck.size();
}

/*ToString
Desc: Used to print out the deck
Params -> deck (vector) - the deck to be printed
Returns -> none
*/
string  Deck::ToString(){
    //Initialize
    string deckString;
    for (Card i : _deck){
        //call the card ToString
        deckString = deckString + i.ToString() + "\n";
    }
    return deckString;
}