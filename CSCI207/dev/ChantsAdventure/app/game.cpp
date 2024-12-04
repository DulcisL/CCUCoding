/**
 * @file Game.cpp
 * @author Lakota Dolce
 * @brief This is the main file for the Chants Adventure Game
 * @version 0.1
 * @date 2024-11-06
 *
 */
#include <iostream>
#include <unistd.h>

#include <Node.hpp>
#include <Asset.hpp>
#include <Player.hpp>
#include <Monster.hpp>
#include <AdventureGameMap.hpp>

using namespace std;
using namespace chants;

/**
* @param: string str - string to see if is number
* @return bool value- if str is number return true else false
*/
bool isNumber(const string &str)
{
    for (char const &c : str)
    {
        if (!std::isdigit(c))
            return false;
    }
    return true;
}

/**
* @param: Node viewPort -  
* @return none
*/
void AtNode(Node &viewPort)
{   
    cout << "\033[2J\033[1;1H"; // clear screen

    // Output contents of this Node
    cout << "Location: " << viewPort.GetName() + "\n\n";
    cout << viewPort.Description << endl
         << "There are paths here ..." << endl;
    for (Node *node : viewPort.GetConnections())
    {
        cout << node->GetId() << " " << node->GetName() << endl;
    }

    // Show all assets in Node
    for (Asset *asset : viewPort.GetAssets())
    {
        cout << "Asset at this node: " << asset->GetName() << " " << asset->GetMessage() << " " << asset->GetValue() << endl;
    }

    // Show any monsters at this Node
    for (Monster *monster : viewPort.GetMonsters())
    {
        cout << "Monster at this node: " << monster->GetName() << " " << monster->GetHealth() << endl;
    }

    cout << "\n";
}

/**
* @param: string loc - location
* @param: vector gamemap - the game nodes in the game
* @return int - The next tile ID being returned
*/
int FindNode(string loc, vector<Node> *map)
{
    int intLoc = -1;
    if (isNumber(loc))
    {
        intLoc = stoi(loc);
    }
    for (Node node : *map)
    {
        if (node.GetName() == loc || node.GetId() == intLoc)
            return node.GetId();
    }
    return -1;
}

/**
* @param: Player player - The player object
* @param: Monster monster -  the Monster object
* @return: int player health
*/
int Battle(Player player, Monster monster)
{
    srand(time(nullptr));

    return player.GetHealth();
}

/**
* @param: string str - The last string entered into command
* @return: string -  A trimmed string 
*/
std::string getLastWord(const std::string &str)
{
    // Trim trailing spaces
    std::string trimmed = str.substr(2);
    return trimmed;
}

/** takeAsset
* @param: Asset asset - the asset being taken
* @param: Player player - The player
* @param: vector<Node> map - The game map
* @param: int nodeId - the node Id number
* @return: none
*/
void takeAsset(string asset, Player& player, vector<Node>* map, int nodeId){
    int index = -1;
    Node& currentNode = (*map)[nodeId];
    vector<Asset*>& assets = currentNode.GetAssets();
    
    //find asset
    for (int i = 0; i < assets.size(); i++){
        if (assets[i]->GetName() == asset){
            //save index
            index = i;
        }
    }
    //Check if asset wasn't found
    if (index != -1){
        cout << "Picking up the asset\n" << endl;
        //add to player if found
        player.AddAsset(*assets[index]);
        //delete from node
        currentNode.RemoveAsset(assets[index]);
    }
    if (index == -1){
        cout << "Asset not found at this location\n" << endl;
    }
}

/** inpectAsset
* @param: Player player - The player
* @return: none
*/
void inpectAsset(Player &player){
    //Initialize variables
    string input;
    int assetIndex = -1;

    //Get the assets
    vector <Asset> assets = player.GetAssets();
    int assetSize = assets.size();

    //Check for no assets
    if(assetSize == 0){
        cout << "No assets to inspect!" << endl;
        return;
    }

    //Print assets
    cout << "Which asset would you like to inspect? \n" << endl;
    for (int i = 0; i < assetSize; i++){
        cout << "Asset (" << i + 1 << ") " << assets[i].GetName() << endl;
    }
    //Get user input for asset to inspect
    getline(cin, input);

    //Convert to int
    if (isNumber(input)){
        assetIndex = stoi(input) - 1;
    }

    //Check for not found condition
    if (assetIndex < 0 || assetIndex > assetSize){
        cout << "Asset Not Found\n" << endl;
    }

    if (assetIndex >= 0){
        cout << "Inspecting asset\n" << endl;
        //Print info about asset
        cout << assets[assetIndex].GetName() << " -> " << assets[assetIndex].GetMessage() << endl;
    }
    
    return;
}
//
// All this game setup will be moved to gamemap and out of the main function
//
int main(){
    try {
        cout << "\033[2J\033[1;1H"; //Clear the screen

        //Make map
        /* Causes bad_alloc fault
        AdventureGameMap map = AdventureGameMap(); 
        vector<Node> gameMap = map.GetLocations();
        */
        vector<Node> gameMap;
        // build all nodes
        Node darkRoom = Node(0, "Dark Room");
        darkRoom.Description = "You open your eyes and to your surprise you are in a dark room. You don't know how or why you got \nhere. as you look around you can see an outline of light around a dark door.\n";

        Node meadow = Node(1, "Meadow");
        meadow.Description = "You look around and see a meadow, a small brook trickles across the green expanse.\n";

        Node forest = Node(2, "Forest");
        forest.Description = "You are deep in a forest. The trees grow like redwoods, hundreds of feet tall and twenty or more feet\n around. \n";

        Node abandonedFarm = Node(3, "Abandoned Farm");
        abandonedFarm.Description = "A small farmhouse sits in a field, the field sits overgrown with weeds and grass, the stone walls\n falling over in places You look at the small house, the room has fallen in and the\n building is tilting to one side. \n";

        Node mountainPass = Node(4, "Mountain pass");
        mountainPass.Description = "As you climb the mountain you come to a pass, as you look around you notice that there is a jagged\n cliff on either side towering above you. There looks to be a cave through one of \nthe cliffs. Looking ahead of you, you see an endless forest.\n It seems to go on forever, overrun with vines and briars it looks ominous and daunting. \nIt doesn't look passable\n";

        Node cave = Node(5, "Cave");
        cave.Description = "As you enter the cave you feel a coldness come over you. There seems to exude an evil from the depths below.\nYou feel a cold damp breeze from the inner parts of the cave. You can only see the \ncorner faintly in the distance.\n";

        Node innerCave = Node(6, "Inner Cave");
        innerCave.Description = "The smell of rotting washes over you as you enter a large chamber. Ahead sits  a pile of something in \nthe center, this must be where the smell is coming from. You also notice what \nappears to be a mirror or picture. As you look at it you realize \nit is moving and a city comes into view through it. \n";

        Node abandonedHouse = Node(7, "Abandoned House");
        abandonedHouse.Description = "The last thing you remeber was touching the floating mirror with the city inside. Now you look \naround and see a house in bad shape. The floor boards are rotted, the cabinets and \ncounters are falling apart from years of neglect. Dust lays\n heavy atop everything except for what appears to be a small path through the dust. \n";

        Node abandonedCity = Node(8, "Abandoned City");
        abandonedCity.Description = "As you leave the abandoned house you notice that the same fate seems to have befallen this city that \nyou are now in. The city is quiet there is no one around and the other building \nand houses all look like they are ready to fall apart. \n";

        Node riverside = Node(9, "Riverside");
        riverside.Description = "A river runs along the outskirts of the city many broken down mills line the shores. There doesn't \nseem to be a way to cross as it is too deep and moving to fast. \n";

        Node path = Node(10, "Path");
        path.Description = "A path goes ahead and continues into the distance. It seems well used and may lead to some kind of civilization and answers as to what is going on. \n";
        
        Node pathFork = Node(11, "Fork");
        pathFork.Description = "You come to a fork in the path it splits into three directions,one to the left, one to the right, and \none straight ahead. You can't tell which way the paths go and there are no signs or \narrows, however the thing that catches your attention is the \ndemon sitting in the middle of the crossroad.\n";
        
        Node city = Node(12, "City");
        city.Description = "As you enter the city you notice the people, they are wearing rags for clothes that may have not been \nwashed in weeks. The people are frail and look weak from malnutrition. They stare at you, \nthe outsider, and watch warily. A few shops dot the city, but only one is open. \n";
        
        Node jail = Node(13, "Jail");
        jail.Description = "A jail sits in front of you all the windows barred and a heavy door on the entrance. As you enter you see \nrows of inmates they sit in the corners of the cells so skinny their you can see their \nbones through their skin. \n";
        
        Node trader = Node(14, "Trader Shop");
        trader.Description = "As you enter the dusty shop, an old man greets you, as you look around the small shop is mostly empty \nexcept a few items. ";
        
        Node castle = Node(15, "Castle");
        castle.Description = "A Desolate Castle sits at the center of the town, a moat surrounds it and separates it from the town.\n A single draw bridge is down with a guard standing in front.";
        
        Node castleCellar = Node(16, "Castle Cellar");
        castleCellar.Description = "You notice a couple doors leading to the cellar of the castle. There is no lock. When you open the doors you\nsee nothing but darkness.";
        
        Node kitchen = Node(17, "Kitchen");
        kitchen.Description = "The smell of food catches your nose and you follow it to the door to the side. Inside is the kitchen, they \nare preparing a meal for the castle residence.";
        
        Node outerDoor = Node(18, "Outer Door");
        outerDoor.Description = "You enter a large chamber within the castle.As you look around you notice the ornate carpet on the floor, \nthere are mounted animals around hanging from the walls, and a large double door stands in front of you. \nNext to the door stands a guard with a halbert.";
        
        Node throneRoom = Node(19, "Throne Room");
        throneRoom.Description = "As you enter the throne room you see a very large throne sat against the back wall with a window framing the \nseat. You see the outline of a large person sitting on the throne but can't see the persons face as he /nsits in darkness with light of the window behind him";
        

        // connect nodes paths
        darkRoom.AddConnection(&meadow);

        meadow.AddConnection(&darkRoom);
        meadow.AddConnection(&forest);
        meadow.AddConnection(&abandonedFarm);

        abandonedFarm.AddConnection(&meadow);
        abandonedFarm.AddConnection(&forest);
        abandonedFarm.AddConnection(&mountainPass);

        forest.AddConnection(&meadow);
        forest.AddConnection(&abandonedFarm);
        forest.AddConnection(&mountainPass);

        mountainPass.AddConnection(&abandonedFarm);
        mountainPass.AddConnection(&forest);
        mountainPass.AddConnection(&cave);

        cave.AddConnection(&mountainPass); 
        cave.AddConnection(&innerCave);

        innerCave.AddConnection(&cave);
        innerCave.AddConnection(&abandonedHouse); // one way connection

        abandonedHouse.AddConnection(&abandonedCity);
        
        abandonedCity.AddConnection(&abandonedHouse);
        abandonedCity.AddConnection(&riverside);
        abandonedCity.AddConnection(&path);

        riverside.AddConnection(&abandonedCity);
        riverside.AddConnection(&path);

        path.AddConnection(&abandonedCity);
        path.AddConnection(&riverside);
        path.AddConnection(&pathFork);

        pathFork.AddConnection(&path);
        pathFork.AddConnection(&city);
        pathFork.AddConnection(&meadow);
        pathFork.AddConnection(&mountainPass);

        city.AddConnection(&path);
        city.AddConnection(&jail);
        city.AddConnection(&castle);
        city.AddConnection(&trader);

        trader.AddConnection(&city);

        jail.AddConnection(&city);
        jail.AddConnection(&mountainPass); //One Way

        castle.AddConnection(&city);
        castle.AddConnection(&castleCellar);
        castle.AddConnection(&kitchen);
        castle.AddConnection(&outerDoor);
        
        castleCellar.AddConnection(&castle);
        castleCellar.AddConnection(&kitchen);

        kitchen.AddConnection(&castleCellar);
        kitchen.AddConnection(&castle);
        kitchen.AddConnection(&outerDoor);

        outerDoor.AddConnection(&kitchen);
        outerDoor.AddConnection(&throneRoom);

        throneRoom.AddConnection(&outerDoor);
        throneRoom.AddConnection(&jail); //One way if player is defeated

        // build map in same order as Node Ids above.
        // The index of each node in the vector must match it's id.
        gameMap.push_back(darkRoom);
        gameMap.push_back(meadow);
        gameMap.push_back(forest);
        gameMap.push_back(abandonedFarm);
        gameMap.push_back(mountainPass);
        gameMap.push_back(cave);
        gameMap.push_back(innerCave);
        gameMap.push_back(abandonedHouse);
        gameMap.push_back(abandonedCity);
        gameMap.push_back(riverside);
        gameMap.push_back(path);
        gameMap.push_back(pathFork);
        gameMap.push_back(city);
        gameMap.push_back(trader);
        gameMap.push_back(jail);
        gameMap.push_back(castle);
        gameMap.push_back(castleCellar);
        gameMap.push_back(kitchen);
        gameMap.push_back(outerDoor);
        gameMap.push_back(throneRoom);
        
        // build assets
        Asset torch("Torch", "A torch can be very useful, especially in dark places.", 50, false);
        Asset knife("Knife", "A knife to help defend yourself", 150, true);
        Asset healthPotion("Health Potion", "A potion that that heals a small amount of health.", 250, false);
        Asset goldCoin("Gold Coin", "Could be worth something", 100, false);
        Asset poison("Poison", "A deadly green fluid sloshes around inside the glass bottle.", 50, true);

    
        // randomly add assets to nodes
        int numOfNodes = gameMap.size();

        srand(time(nullptr)); // seed the random number generator
        
        int count = 0;
        int randNode = rand() % numOfNodes;
        gameMap[randNode].AddAsset(&goldCoin);
        randNode = rand() % numOfNodes;
        gameMap[randNode].AddAsset(&poison);

        gameMap[darkRoom.GetId()].AddAsset(&torch);
        gameMap[meadow.GetId()].AddAsset(&knife);
        gameMap[meadow.GetId()].AddAsset(&healthPotion);
        
        // build monsters
        // randomly add monsters to nodes
        // nameofmonster("Name", Health, FightCoefficient)
        Monster wolf("Wolf", 4000, 100);
        Monster knight("Knight", 5000, 100);
        Monster dwarf("Dwarf", 6000, 100);
        Monster demon("Demon", 4000, 100);
        Monster dragon("Dragon", 7000, 100);
        Monster king("King", 8000, 100);

        randNode = rand() % numOfNodes;
        gameMap[randNode].AddMonster(&wolf);

        randNode = rand() % numOfNodes;
        gameMap[randNode].AddMonster(&dwarf);

        randNode = rand() % numOfNodes;
        gameMap[randNode].AddMonster(&demon);
        
        //Add boss and special Characters to specific nodes
        gameMap[pathFork.GetId()].AddMonster(&demon);
        gameMap[innerCave.GetId()].AddMonster(&dragon);
        gameMap[throneRoom.GetId()].AddMonster(&king);
        
        // get ready to play game below
        int nodePointer = 0; // start at home
        bool exit = false;
        string input;
        Player player("Player", 5000, 100);

        // +++++++++ game loop ++++++++++
        while (exit == false){

            
            bool error = false;
            // show current node info
            AtNode(gameMap[nodePointer]);
            cout << "What would you like to do? \n(t)ake an asset \n(a)ttack a monster \n(d)rop an asset \n(i)nspect an asset \nGo to node? \ne(x)it: ";
            getline(cin, input);

            //check length of input
            if (input.size() <= 0){
                cout << "That was not a valid input\n";
                continue;
            }
            string lastWord;
            int nodeAddr = -1;
            int dir = -1;
            switch (input[0]){
                case 't':
                    lastWord= getLastWord(input);
                    cout << "Taking: " << lastWord << endl; 
                    takeAsset(lastWord, player, &gameMap, nodePointer);
                    sleep(5);
                    break;
                case 'a':
                    lastWord= getLastWord(input);
                    cout << "Attacking: " << lastWord << endl;
                    sleep(5);
                    break;
                case 'd': 
                    lastWord= getLastWord(input);
                    cout << "Dropping: " << lastWord << endl;
                    sleep(5);
                    break;
                case 'i': 
                    cout << "Inspecting " << endl;
                    inpectAsset(player);
                    sleep(5);
                    break;
                case 'x':
                    exit = true;
                    break;
                //Otherwise check for node change input
                default:
                    if (isNumber(input)){
                        nodeAddr = stoi(input);
                    }
                    //Check if valid connection
                    bool validConnection = false;
                    for (Node* node : gameMap[nodePointer].GetConnections())
                    {
                        if (node->GetId() == nodeAddr){
                            validConnection = true;
                            break;
                        }
                    }

                    //if valid connection change to node
                    if (validConnection){
                        dir = FindNode(input, &gameMap);
                    }
                    cout << "Dir: " << dir << endl;
                    if (dir >= 0)
                        nodePointer = dir;
                    else
                        cout << "Not a valid node address\n";

                    cout << endl;
                    break;
            }
        }
        return 0;
    }
    catch (const std::exception &e) { cout << "Exception caught: " << e.what() << endl; } 
    catch (...) { cout << "Unknown exception caught" << endl;}
}
