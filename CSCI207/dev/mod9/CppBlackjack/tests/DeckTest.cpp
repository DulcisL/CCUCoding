/**
 * @file DeckTest.cpp
 * @author Lakota Dolce
 * @brief This is the test file for the deck.cpp
 * @version 0.1
 * @date 2024-10-08
 *
 */
#include "Deck.h"

#include <stdio.h>
#include <stdexcept>
#include <string>
#include <iostream>


int main (){
    //Create a deck
    Deck deck1;

    //set up loop
    int dealt = 0;
    cout << "The size of the deck: " << deck1.sizeOf() << endl;
    //Deal 4 cards
    while (dealt < 4 && deck1.sizeOf() != 0){
        cout << "\n";
        try{
            cout << deck1.deal().ToString() << endl;
            dealt +=1 ;
        }
        catch (out_of_range){
            cout << "Out of cards\n" ;
            break;
        }
    }
    cout << "The size of the deck: " << deck1.sizeOf() << endl;
    return 0;
}