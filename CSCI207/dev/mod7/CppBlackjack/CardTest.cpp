#include <iostream>
#include <vector>
#include "Card.h"
using namespace std;

/*CreateDeckOfCard
Desc: Creates 52 individual cards by way of a nested for loop and stores it in the deck vector
Params -> deck (Vector) - contains the array to be used to store the deck (passed by reference)
Return -> none
*/
void CreateDeckOfCard(vector<Card> &deck){
    //run 13 times to make card
    for (int i = 1; i < 14; i ++){
        //run 4 times to get suits
        for (int j = 1; j < 5; j++){
            //make the card
            Card card = Card(i,j,true);
            //push the card to the vector
            deck.push_back(card);
        }
    }
}
/*ToString
Desc: Used to print out the deck
Params -> deck (vector) - the deck to be printed
Returns -> none
*/
void ToString(vector<Card> deck){
    for (Card i : deck){
        //call the card ToString
        cout << i.ToString() << "\n";
    }
}

/*Shuffle
Desc: Shuffles the deck to be random
Params -> deck (vector) - Store the deck to be shuffled (passed by reference)
          numShuffles - number of times for the deck to be shuffled
Returns -> none
*/
void Shuffle(vector<Card> &deck, int numShuffles){
    //seed the rand
    srand(time(NULL));

    //set up loop
    int indice1;
    int indice2;
    int i = 0;
    while (i < numShuffles){

        //get indices use modulo to keep within deck size
        indice1 = i % deck.size();
        indice2 = rand() % deck.size();

        //swap places
        swap(deck[indice1], deck[indice2]);
        i++;
    }   
}

/*deal
Desc: Deals cards to the user and removes them from the vector
Params -> Vector<Card> deck - Contains the deck of cards (passed by reference)
          int numCards - The number of cards to be dealt
Returns -> none
*/
void deal(vector<Card> &deck, int numCards){
    //Check if numCards is equal to zero and ensure there is space in the deck to deal
    if(numCards != 0 && deck.size() >= numCards){

        //Inform player
        cout << "Dealing cards... \n";

        //Create loop
        for (int i = 0; i < numCards && !deck.empty(); i++){

            //Get the card at the beginning
            Card card = deck.back();

            //erase the card at the beginning
            deck.pop_back();

            //print the card
            cout << card.ToString() << endl;
        }
    }
}

/*main
Desc: Contains the main function
Params -> none
Returns -> int for success
*/
int main()
{
    //Test with one card
    Card card(1, 1, true);
    cout << card.ToString() << endl;

    //Initialize
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

    return 0;
}