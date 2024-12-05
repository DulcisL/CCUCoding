/**
 * @file Player.cpp
 * @author Lakota Dolce
 * @brief This is a main file for the Adventure Game Map
 * @version 0.1
 * @date 2024-11-06
 *
 */
#include <Monster.hpp>

namespace chants
{
    Monster::Monster(string name, int health, int fightCoefficient) : Combatant(name, health, fightCoefficient)
    {
    }
}