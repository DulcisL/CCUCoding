#include <Combatant.hpp>
#include <time.h>

using namespace std;

namespace chants
{
    Combatant::Combatant(string name, int health, int fightCoefficient)
    {   
        _name = name;
        if (health > 0){
            _health = health;
        }
        if (health <= 0){
            throw std::runtime_error("Health value cannot be below 0");
        }
        _fightCoefficient = fightCoefficient;
    }

    string Combatant::GetName()
    {
        return _name;
    }

    int Combatant::GetHealth()
    {
        return _health;
    }

    /// @brief Average fight value over several interations
    /// @return
    int Combatant::Fight()
    {
        int subTotal = 0;
        srand(time(nullptr));
        for (int i = 0; i < _fightCoefficient; i++)
        {
            subTotal += rand() % _fightCoefficient;
        }
        float Total = subTotal / _fightCoefficient;
        return (int)Total;
    }
    int Combatant::GetFightCoefficient(){
        return _fightCoefficient;
    }
}
