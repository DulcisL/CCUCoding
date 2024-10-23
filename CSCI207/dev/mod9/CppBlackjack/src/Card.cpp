/**
 * @file Card.cpp
 * @author Lakota Dolce
 * @brief This is the definition (source) file for a playing Card.
 * @version 0.1
 * @date 2024-09-25
 *
 *
 */
#include "Card.h" //Include the header file
#include <stdexcept>

/**
 * @brief Parameterized Construct a new Card
 *
 * @param value - is a number between 1 and 13, Ace (11), 2 - 10, Jack (10), Queen (10), King (10)
 * @param suit - is a number between 1 and 4, Clubs, Diamonds, Hearts, Spades
 * @param isFaceUp - true or false
 */
Card::Card(int value, int suit, bool isFaceUp)
{
    try
    {
        if (value < 1 || value > 13)
            throw std::runtime_error("Card value out of range. Must be 1 - 13");

        if (suit < 1 || suit > 4)
            throw std::runtime_error("Suit value out of range. Must be 1 - 4");

        _value = value;
        convertValueToString(value);

        // if Jack, Queen, or King, set to 10
        if (value > 10)
        {
            _value = 10;
        }
        // if 1 (Ace) lets set it to 11 by default
        if (value == 1)
        {
            _value += 10;
        }

        _suit = suit;
        convertSuitToString(suit);

        this->isFaceUp = isFaceUp;
    }
    catch (const std::exception &e)
    {
        throw e;
    }
}

/**
 * @brief return the numeric value of the card
 *
 * @return int
 */
int Card::GetValue() // Scope resolution operator 
{
    return _value;
}

/**
 * @brief converts the card integer to a string representation,
 *          example: 1 = Ace, 11 = Jack, 12 = Queen, 13 = King
 *
 * @param val - number 1 - 13
 */
void Card::convertValueToString(int val)
{
    switch (val)
    {
    case 1:
        _strValue = "ACE";
        break;
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 8:
    case 9:
    case 10:
        _strValue = to_string(val);
        break;
    case 11:
        _strValue = "JACK";
        break;
    case 12:
        _strValue = "QUEEN";
        break;
    case 13:
        _strValue = "KING";
        break;
    default:
        throw "Card value must be between 1 and 13.";
    }
}

/**
 * @brief converts the suit integer to a string representation,
 *          example: 1 = Clubs, 2 = Diamonds, 3 = Hearts, 4 = Spades
 *
 * @param val - number 1 - 4
 */
void Card::convertSuitToString(int suit)
{
    switch (suit)
    {
    case 1:
        _strSuit = "CLUBS";
        break;
    case 2:
        _strSuit = "DIAMONDS";
        break;
    case 3:
        _strSuit = "HEARTS";
        break;
    case 4:
        _strSuit = "SPADES";
        break;
    default:
        throw "Suit must be a value between 1 and 4.";
    }
}

/**
 * @brief Simple string output that represents this playing card face up or face down
 *
 * @return string - card representation
 */
string Card::ToString()
{
    string temp = "";
    if (isFaceUp)
        temp = _strValue + " " + _strSuit;
    else
        temp = "Face-down";
    return temp;
}