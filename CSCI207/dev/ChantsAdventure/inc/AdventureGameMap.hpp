/**
 * @file AdventureGameMap.hpp
 * @author Lakota Dolce
 * @brief This is the hpp file for the Adventure map
 * @version 0.1
 * @date 2024-11-06
 *
 */
#pragma once

#include <string>
#include <Node.hpp>

using namespace std;

namespace chants
{
    class AdventureGameMap
    {
    private:
        vector<Node> locations;
        /**
        * @param: none
        * @return: none
        */
        void buildMapNodes();

    public:
        
        /**
        * @param: none
        * @return: none
        */
        AdventureGameMap();
        /**
        * @param: none
        * @return: vector - locations
        */
        vector<Node> GetLocations();
    };
}