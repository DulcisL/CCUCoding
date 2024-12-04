/**
 * @file Monster.hpp
 * @author Lakota Dolce
 * @brief This is the hpp file for the Monster.cpp file
 * @version 0.1
 * @date 2024-11-06
 *
 */
#pragma once

#include <string>
#include <Combatant.hpp>

using namespace std;

namespace chants
{
    class Monster : public Combatant
    {
    public:
        /** Paramaterize Constructor
        * @param: string name -  The name of the Monster
        * @param: int health - the health of the monster
        * @param: int fightCoefficient - 
        * @return: none
        */
        Monster(string name, int health, int fightCoefficient);
    };
}