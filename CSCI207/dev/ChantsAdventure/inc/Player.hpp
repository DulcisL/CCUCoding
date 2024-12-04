/**
 * @file Player.hpp
 * @author Lakota Dolce
 * @brief This is the hpp file for the player.cpp file
 * @version 0.1
 * @date 2024-11-06
 *
 */
#pragma once

#include <string>
#include <vector>
#include <iostream>
#include <Asset.hpp>
#include <Combatant.hpp>

using namespace std;

namespace chants
{
    class Player : public Combatant
    {
    private:
        vector<Asset> _assets;

    public:
        /** Parameterize Constructor
        * @param: string name - The name of the player
        * @param: int health - The health of the player
        * @param: int fightCoefficient -  The Fight coefficient of the player
        * @return: none
        */
        Player(string name, int health, int fightCoefficient);

        /**
        * @param: Asset asset - The asset to be added
        * @return: none
        */
        void AddAsset(Asset asset);

        /**
        * @param: none
        * @return: vector<Asset> _assets - The vector of assets in player inventory
        */
        vector<Asset> GetAssets();
        /**
        * @param: none
        * @return: int value -  The total value of the assets
        */
        int GetTotalAssetValue();
    };
}
