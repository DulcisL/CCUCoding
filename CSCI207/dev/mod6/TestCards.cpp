#include <iostream>
#include <vector> 
#include "Card.h" //allow access to other files

using namespace std;

//build a deck of cards
int main(){
    //Card card(2, "Hearts", true);

    //calling with different constructors
    //Can overload functions as long as the signatures are different
    //Signature is made of the FunctionName, NumParam, OrderParam, ParamType (Not the return type)
    /*runtime_error
    Card Card1 = card(); //Uses Default constructor
    Card Card2 = card(3,4, true); Uses Parameter constructor
    Card Card3 = card(Card2); //Uses a Copy constructor
    */

    //generate deck
    vector<Card> deck;
    for (int i = 1; i < 13; i++){
        for (int y; y < 4; y++){
            Card card(i,y, true);
            deck.push_back(card);
        }
    }
    
    //Print the deck out
    for (Card card : deck){
        cout << card.ToString();
    }

    //Card arr[52]; give a weird value to the cards and must be predetermined in size
    //cout << card._value << endl;
    //vector expands or contracts as needed

}