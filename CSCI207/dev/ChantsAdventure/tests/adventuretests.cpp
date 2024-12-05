/**
 * @file Player.cpp
 * @author Lakota Dolce
 * @brief This is a Unit Test Fixture to the Player class
 * @version 0.1
 * @date 2024-11-06
 *
 */
#include <gtest/gtest.h>
#include <vector>

#include <Node.hpp>
#include <AdventureGameMap.hpp>
#include <Player.hpp>
#include <Combatant.hpp>
#include <Monster.hpp>

// https://google.github.io/googletest/reference/assertions.html

/**
 * @brief Test parameterized constructor that creates a valid Player object.
 *      In this case, a Player is created with "TEST" name, 100 health, 100 FightingCoefficient.
 */
TEST(PlayerTest, ValidPlayer)
{
    try{
        chants::Player player("TEST", 100, 100);
        EXPECT_EQ(player.GetName() , "TEST");
        EXPECT_EQ(player.GetHealth() , 100);
        EXPECT_EQ(player.GetFightCoefficient() , 100);
    }
    catch(const std::exception &e){
        FAIL();
    }
}
/**
 * @brief Test parameterized constructor that creates a invalid Player object.
 *      In this case, an invalid instance of a Player is created with "TEST" name, -1 health, 100 FightingCoefficient.
 */
TEST(PlayerTest, InvalidPlayerHealthBelowZero)
{
    try{
        //create an invalid player health
        chants::Player player("TEST", -1, 100);
        FAIL();
    }
    catch(const std::exception &e){
        SUCCEED();
    }
}

/**
 * @brief Test add asset to player
 *      In this case, a Player is created with "TEST" name, 100 health, 100 FightingCoefficient.
 *      An asset is created with "NAME" name, "DESC" description, 100 value, false isOffensive
 *      Asset is added to player inventory then checked
 */
TEST(PlayerTest, AddValidAsset){
    try{
        //create player
        chants::Player player("TEST", 100, 100);
        //create asset
        chants::Asset asset("NAME", "DESC", 100, false);
        //add asset to player
        player.AddAsset(asset);
        //get players assets
        vector<chants::Asset> assets =  player.GetAssets();

        //Check asset values are the same as original
        EXPECT_EQ(assets[0].GetName(), asset.GetName());
        EXPECT_EQ(assets[0].GetMessage(), asset.GetMessage());
        EXPECT_EQ(assets[0].GetValue(), asset.GetValue());
        EXPECT_EQ(assets[0].isOffensive(), asset.isOffensive());
    }
    catch (const std::exception &e){
        FAIL();
    }
}

/**
 * @brief Test Asset Total Value
 *      In this case, a Player is created.
 *      An assets are created with 100 for values
 *      Assets are added to player inventory and value total should be 400
 */
TEST(PlayerTest, GetTotalAssetValue){
    //create player
    chants::Player player("TEST", 100, 100);
    //create assets and add to a vector
    chants::Asset asset1("NAME1", "DESC1", 100, false);
    chants::Asset asset2("NAME2", "DESC2", 100, false);
    chants::Asset asset3("NAME3", "DESC3", 100, false);
    chants::Asset asset4("NAME4", "DESC4", 100, false);
    vector<chants::Asset> assets;

    assets.push_back(asset1);
    assets.push_back(asset2);
    assets.push_back(asset3);
    assets.push_back(asset4);

    for (int i = 0; i < assets.size(); i++){
        player.AddAsset(assets[i]);
    }
    EXPECT_EQ(player.GetTotalAssetValue(), 400);
}   
