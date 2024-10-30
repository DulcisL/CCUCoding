/**
 * @file Player.cpp
 * @author Lakota Dolce
 * @brief This is the definition (source) file for a player
 * @version 0.1
 * @date 2024-10-08
 *
 */
#include "Player.h"
#include "Card.h"
#include "Deck.h"

#include <vector>
#include <string.h>
#include <stdexcept>
#include <iostream>

/// @brief The constructor for setting up the class
/// @param string nameIn - takes the name of the player
/// @param int thresholdIn  - takes the players cut off for taking cards
///         
Player::Player(string nameIn, int thresholdIn){
    //set attributes
    _name = nameIn;
    threshold = thresholdIn;
}

//Getters
/// @brief GetName - used to get the name of the player
/// @return - Return a string of the player name
///
string Player::GetName(){
    return _name;
}

/// @brief GetHand - gets the hand of the player
/// @return - Return a vector of the players hand
///
vector<Card> Player::GetHand(){
    return _hand;
}

//Functions 

/// @brief Deal used to add a card to the persons hand
/// @param vector Deck - Holds the deck the game is being played from
///
void Player::Deal(vector<Deck> Deck){
    _hand.push_back(Deck.deal());
    return;
}

/// @brief Check score of current hand
///
int Player::CalculateScore(){
    int total = 0;
    //get the value of each card and add to score
    for (Card c: _hand){
        total += c.GetValue();
    }
    return total;
}

/// @brief Gets the number of cards in a players hand
///
int Player::NumCards(){
    return _hand.size();
}

/// @brief The ToString used to print out the person class
///
string Player::ToString(){
    string temp;
    temp += "\nName: " + _name + "\nHand: {"; 
    for (Card c: _hand){
        temp += c.ToString() + ", ";
    }
    temp += " }\nStatus: " + status;
    return temp;
}