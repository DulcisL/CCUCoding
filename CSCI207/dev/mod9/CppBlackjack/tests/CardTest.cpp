#include <iostream>
#include <vector>
#include "Card.h"
using namespace std;



/*main
Desc: Contains the main function
Params -> none
Returns -> int for success
*/
int main(){
    //Test with one card
    Card card(1, 1, true);
    cout << card.ToString() << endl;

    /*//Initialize
    vector<Card> deck;
    int numShuffles = 1000;
    int numDealt = 4;

    //Create the deck
    cout << "\ncreating deck \n";
    CreateDeckOfCard(deck);

    //Print the deck
    cout << "\nThis is the deck before shuffling: \n";
    ToString(deck);

    //Shuffle the deck
    cout << "\nShuffling the deck \n";
    Shuffle(deck, numShuffles);

    //Print the shuffled deck
    cout << "\nThis is the deck after shuffling: \n";
    ToString(deck);
    

    //Deal 4 cards
    //check size before
    cout << "\nThe size before dealing: " << deck.size() << endl;
    //deal
    deal(deck, numDealt);

    //The size after dealing
    cout << "\nThe size after dealing: " << deck.size() << endl;
    */
    return 0;
}