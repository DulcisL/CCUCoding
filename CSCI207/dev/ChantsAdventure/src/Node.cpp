/**
 * @file Player.cpp
 * @author Lakota Dolce
 * @brief This is a main file for the Adventure Game Map
 * @version 0.1
 * @date 2024-11-06
 *
 */
#include <Node.hpp>

namespace chants
{

    Node::Node(int id, string name)
    {
        _id = id;
        _name = name;
    }

    int Node::GetId()
    {
        return _id;
    }

    void Node::SetId(int id)
    {
        _id = id;
    }

    string Node::GetName()
    {
        return _name;
    }

    void Node::AddConnection(Node *conn)
    {
        _connections.push_back(conn);
    }

    vector<Node *> Node::GetConnections()
    {
        return _connections;
    }

    Node *Node::GetAConnection(int connId)
    {
        return _connections[connId];
    }

    void Node::AddAsset(Asset *asset)
    {
        _assets.push_back(asset);
    }

    vector<Asset *>& Node::GetAssets()
    {
        return _assets;
    }

    bool Node::operator==(const Node &rhs) const
    {
        return _name == rhs._name;
    }

    void Node::AddMonster(Monster *monster)
    {
        _monsters.push_back(monster);
    }

    vector<Monster *> Node::GetMonsters()
    {
        return _monsters;
    }

    void Node::RemoveAsset(Asset *asset){
        //find asset
        for (int i = 0; i < _assets.size(); i++){
            if (asset == _assets[i]){
                _assets.erase(_assets.begin() + i);
                break;
            }
        } 
    }
}