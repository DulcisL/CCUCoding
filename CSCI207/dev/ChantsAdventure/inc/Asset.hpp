/**
 * @file Asset.hpp
 * @author Lakota Dolce
 * @brief This is the hpp file for the Asset.cpp file
 * @version 0.1
 * @date 2024-11-06
 *
 */
#pragma once

#include <string>

using namespace std;

namespace chants
{
    class Asset
    {
    private:
        string _name;
        string _message;
        int _value;
        bool _isOffensive;

    public:
        bool hasBeenUsed;
        
        /** Parameterize Constructor
        * @param: string name - The name of the asset
        * @param: string  message - The description of the asset
        * @param: int value - The value of the asset
        * @param: bool isOffensive - The bool of whether it can be used in combat
        * @return: none
        */
        Asset(string name, string message, int value, bool isOffensive);
        /**
        * @param: none
        * @return: string name -  The name of the asset
        */
        string GetName();

        /**
        * @param: none
        * @return: string message - The description of the asset
        */
        string GetMessage();

        /**
        * @param: none
        * @return: int value -  The value of the asset
        */
        int GetValue();

        /**
        * @param: none
        * @return: bool - true or false for if object is usable in combat
        */
        bool isOffensive();
    };
}