/**
 * @file Person.h
 * @author Lakota Dolce
 * @brief This is the include (header) file for a player.
 * @version 0.1
 * @date 2024-09-25
 *
 *
 */
#pragma once

#include "Player.h"
#include "Card.h"
#include "Deck.h"

#include <vector>
#include <string.h>
#include <stdexcept>
#include <iostream>
using namespace std;

class Player{
    private:
    /// @brief _name is a string containing the first name of the player
    ///         
    ///         The string is set in the constructor
    string _name;

    /// @brief _hand is a vector containing the cards in the persons hand
    ///         
    ///         The vector is set in the constructor
    vector <Card> _hand;

    public:
    
    //constructor

    /// @brief The constructor for setting up the class
    /// @param string nameIn - takes the name of the player
    /// @param int thresholdIn  - takes the players cut off for taking cards
    ///         
    Player(string nameIn, int thresholdIn);

    /// @brief status - a string containing the status of the player if they win/lost/busted
    ///         
    ///             Set by game logic at the end of the round
    string Status;

    /// @brief threshold is a int containing the max score the player will take hits if below
    ///         
    ///         The int is set in the constructor
    int Threshold;

    /// @brief GetName - used to get the name of the player
    /// @return - Return a string of the player name
    ///
    string GetName();
    
    /// @brief GetHand - gets the hand of the player
    /// @return - Return a vector of the players hand
    ///
    vector<Card> GetHand();

    //Functions 

    /// @brief Deal used to add a card to the persons hand
    /// @param vector Deck - Holds the deck the game is being played from
    ///
    void Deal(Deck &deck);

    /// @brief Check score of current hand
    ///
    int CalculateScore();

    /// @brief Gets the number of cards in a players hand
    ///
    int NumCards();

    /// @brief The ToString used to print out the person class
    ///
    string ToString();

};