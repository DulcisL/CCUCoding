/**
 * @file Player.cpp
 * @author Lakota Dolce
 * @brief This is a main file for the Adventure Game Map
 * @version 0.1
 * @date 2024-11-06
 *
 */
#include <Player.hpp>

namespace chants
{

    Player::Player(string name, int health, int fightCoefficient) : Combatant(name, health, fightCoefficient)
    {
    }

    void Player::AddAsset(Asset asset)
    {
        _assets.push_back(asset);
    }
    vector<Asset> Player::GetAssets()
    {
        return _assets;
    }

    int Player::GetTotalAssetValue()
    {
        int val = 0;
        for (Asset asset : _assets)
        {
            val += asset.GetValue();
        }
        return val;
    }
}