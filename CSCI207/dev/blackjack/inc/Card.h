#include <string>

using namespace std;

//struct is public object
class Card{
    int _value;
    int _suit;
    string _strValue;
    //string _color; Not needed for blackjack
    bool _isFaceUp; //Generally bools look like questions
    //functionality
    //because public no need for getter or setters
    //Constructor

    void convertSuitToString(){

    }
    void convertValueToString(){

    }
    
    public: //Declare everything below as public
    Card(int value, int suit, bool isFaceUp){
        //ensure that the variable is assigned to the object you can use this-> or change name, be consistent though
        _value = value;  
        _suit = suit;
        _isFaceUp = isFaceUp;

    }
    string ToString(){
        return to_string(_value) + " "+ to_string(_suit);
    }
    
};