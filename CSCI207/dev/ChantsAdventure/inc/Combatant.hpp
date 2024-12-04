/**
 * @file Combatant.hpp
 * @author Lakota Dolce
 * @brief This is the hpp file for the Combatant.cpp file
 * @version 0.1
 * @date 2024-11-06
 *
 */
#pragma once
#include <string>
#include <iostream>
using namespace std;

namespace chants
{
    class Combatant
    {
    protected:
        string _name;
        int _health;
        int _fightCoefficient;

    public:
        /** Paramaterize Constructor
        * @param: string name: the name of the combatant
        * @param: int healt: the health of the combatant
        * @param: int coefficient: 
        * @return: none
        */
        Combatant(string name, int health, int coefficient);

        /**
        * @param: none
        * @return: int - 
        */
        int Fight();

        /**
        * @param: none
        * @return: string name -  The name of the combatant
        */
        string GetName();

        /**
        * @param: none
        * @return: int health - The health of the combatant
        */
        int GetHealth();
        /**
        * @param: none
        * @return: int fightCoefficient - The fight coefficient of the combatant
        */
        int GetFightCoefficient();
    };
}