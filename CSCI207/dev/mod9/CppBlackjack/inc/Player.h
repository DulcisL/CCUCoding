/**
 * @file Person.h
 * @author Lakota Dolce
 * @brief This is the include (header) file for a person.
 * @version 0.1
 * @date 2024-09-25
 *
 *
 */
#pragma once

#include "Card.h"

#include <vector>
#include <string>
using namespace std;

class Person{
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

    /// @brief The constructor for setting up the class
    ///         
    Person();

    /// @brief Deal used to add a card to the persons hand
    ///
    Deal();

    /// @brief Check score of current hand
    ///
    CalculateScore();

    /// @brief Gets the number of cards in a players hand
    ///
    NumCards();

    /// @brief The ToString used to print out the person class
    ///
    ToString();

}