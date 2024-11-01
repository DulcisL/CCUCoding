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
 * @brief Construct a new Deck
 *
 * @param None
 */
Deck::Deck (){
    //Create the deck 
    buildDeck(1, false);
}
/**
 * @brief Parameterized Construct a new Deck
 *
 * @param int numDecks - the number of decks needed for the game
 * @param bool isFaceUp - If the deck should be face up (false) or face down(true)
 */
Deck::Deck(int numDecks, bool isFaceUp){
    //Build a new deck with the number of decks needed
    buildDeck(numDecks, isFaceUp);
}

/** buildDeck
* @desc: Creates 52 individual cards by way of a nested for loop and stores it in the deck vector
* @param - decksNeeded - int contains the number of decks needed to play the game
* @param - isFaceUp - bool containing the value if the cards should be face up or down.
* @return - none
*/
void Deck::buildDeck(int decksNeeded, bool isFaceUp){
    int count = 0;
    while (count < decksNeeded){
        //run 13 times to make card
        for (int i = 1; i < 14; i ++){
            //run 4 times to get suits
            for (int j = 1; j <= 4; j++){
                //make the card
                Card card = Card(i, j, isFaceUp);
                //push the card to the vector
                _deck.push_back(card);
            }
        }
        count ++;
    }
    //Shuffle the deck
    shuffle();
}

/** shuffle
* @desc: Shuffles the deck to be random
* @param - deck (vector) - Store the deck to be shuffled (passed by reference)
* @param - numShuffles - number of times for the deck to be shuffled
* @return - none
*/
void Deck::shuffle(){
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

/** Deal
* @desc: Deals cards to the user and removes them from the vector
* @param Vector<Card> deck - Contains the deck of cards (passed by reference)
* @param int numCards - The number of cards to be dealt
* @return - none
*/
Card Deck::Deal(){
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

/** SizeOf
* @desc: returns the size of the deck
* @param -> none
* @return -> int size of deck
*/
int Deck::SizeOf(){
    return _deck.size();
}

/** ToString
* @desc: Used to print out the deck
* @param -> deck (vector) - the deck to be printed
* @return -> none
*/
string  Deck::ToString(){
    //Initialize
    string deckString;
    for (Card c : _deck){
        //Flip the card
        if (c.isFaceUp == false){
            c.isFaceUp = true;
            //call the card ToString
            deckString = deckString + c.ToString() + "\n";
            //Flip card back
            c.isFaceUp = false;
        }
        else{
            //call the card ToString
            deckString = deckString + c.ToString() + "\n";
        }
        
        
    }
    return deckString;
}