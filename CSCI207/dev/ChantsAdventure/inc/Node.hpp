/**
 * @file Node.hpp
 * @author Lakota Dolce
 * @brief This is the hpp file for the Node.cpp file
 * @version 0.1
 * @date 2024-11-06
 *
 */
#pragma once

#include <vector>
#include <string>
#include <Asset.hpp>
#include <Monster.hpp>

using namespace std;

namespace chants
{

    class Node
    {
    private:
        int _id;
        string _name;
        vector<Node *> _connections;
        vector<Asset *> _assets;
        vector<Monster *> _monsters;

    public:
        string Description;

        /** Parameterized Constructor
        * @param: int id - The ID of the node
        * @param: string name - The name of the Node
        * @return:none
        */
        Node(int id, string name);

        /**
        * @param: none
        * @return: int ID - The id of the node
        */
        int GetId();
        
        /**
        * @param: int ID - The new ID of the node
        * @return: none
        */
        void SetId(int id);

        /**
        * @param: none
        * @return: string Name -  The name of the node
        */
        string GetName();

        /**
        * @param: Node conn -  The node to connect
        * @return: none
        */
        void AddConnection(Node *conn);

        /**
        * @param: none
        * @return: vector Node - The connected nodes
        */
        vector<Node *> GetConnections();

        /**
        * @param: int connID - The ID of the connected tile
        * @return: Node tile - the connected tile
        */
        Node *GetAConnection(int connId);

        /**
        * @param: Asset asset -  The asset
        * @return: none
        */
        void AddAsset(Asset *asset);

        /**
        * @param: none
        * @return: Vector assets - The assets on the tile
        */
        vector<Asset *>& GetAssets();

        /**
        * @param: Monster monster - The monster to be added to the tile
        * @return: none
        */
        void AddMonster(Monster *monster);

        /**
        * @param: none
        * @return: vector monsters - The monsters on the tile
        */
        vector<Monster *> GetMonsters();

        /**
        * @param: Asset asset -  The asset
        * @return: none
        */
        void RemoveAsset(Asset *asset);
        
        bool operator==(const Node &rhs) const;
    };
}