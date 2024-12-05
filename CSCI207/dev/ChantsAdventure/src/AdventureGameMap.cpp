/**
 * @file Player.cpp
 * @author Lakota Dolce
 * @brief This is a main file for the Adventure Game Map
 * @version 0.1
 * @date 2024-11-06
 *
 */
#include <AdventureGameMap.hpp>
#include <Asset.hpp>
#include <Monster.hpp>


#include <iostream>

namespace chants
{
    AdventureGameMap::AdventureGameMap()
    {
        buildMapNodes();

        /*
        Possible assets:

        -	Torch -  An Item used to see in the dark
        -	Knife -  A basic weapon to be used in combat
        -	Health Potion -  An item to be consumed by the player to increase their health
        -	Poison - An item that can be used by the player to decrease their own health or that of a  monster
        -	Sword - A more advanced weapon to be used in combat
        -	Bow -  A weapon to be used in combat requires arrows to be used
        -	Arrow - Ammunition for the bow
        -	Shield - An item that can be used to reduce damage
        -	Armor - an item that can be used to reduce damage
        -	Gold - The currency of the game
        -	Axe - An item that can be used as a weapon or a tool
        -	Staff -  An advanced weapon that uses magic to damage monsters
        -	Stick - A secret weapon found in the game 
        

        Possible monsters:

        -	Demon - A demon, beware of deals
        -   Wolves - Wild animals found all over, generally agressive, watch out for packs fo them.
        -	Dwarves – creatures of the cave obsessed with shiny objects, don't take kindly to trespassers. 
        -   Dragons - Hoarder of treasure, Generally found in caves when not in the air.
        -	Knight – Guards of the castle 
        -	King – Malicious ruler of the lands of 
        */ 
        
    }

    void AdventureGameMap::buildMapNodes()
    {
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
        locations.push_back(darkRoom);
        locations.push_back(meadow);
        locations.push_back(forest);
        locations.push_back(abandonedFarm);
        locations.push_back(mountainPass);
        locations.push_back(cave);
        locations.push_back(innerCave);
        locations.push_back(abandonedHouse);
        locations.push_back(abandonedCity);
        locations.push_back(riverside);
        locations.push_back(path);
        locations.push_back(pathFork);
        locations.push_back(city);
        locations.push_back(trader);
        locations.push_back(jail);
        locations.push_back(castle);
        locations.push_back(castleCellar);
        locations.push_back(kitchen);
        locations.push_back(outerDoor);
        locations.push_back(throneRoom);

        
        // build assets
        Asset torch("Torch", "A torch can be very useful, especially in dark places.", 50, false);
        Asset knife("Knife", "A knife to help defend yourself", 150, true);
        Asset healthPotion("Health Potion", "A potion that that heals a small amount of health.", 250, false);
        Asset goldCoin("Gold Coin", "Could be worth something", 100, false);
        Asset poison("Poison", "A deadly green fluid sloshes around inside the glass bottle.", 50, true);
    
        // randomly add assets to nodes
        int numOfNodes = locations.size();
        srand(time(nullptr)); // seed the random number generator
        
        int count = 0;
        int randNode = rand() % numOfNodes;
        locations[randNode].AddAsset(&goldCoin);
        randNode = rand() % numOfNodes;
        locations[randNode].AddAsset(&poison);

        locations[darkRoom.GetId()].AddAsset(&torch);
        locations[meadow.GetId()].AddAsset(&knife);
        locations[meadow.GetId()].AddAsset(&healthPotion);
        
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
        locations[randNode].AddMonster(&wolf);

        randNode = rand() % numOfNodes;
        locations[randNode].AddMonster(&dwarf);

        randNode = rand() % numOfNodes;
        locations[randNode].AddMonster(&demon);
        
        //Add boss and special Characters to specific nodes
        locations[pathFork.GetId()].AddMonster(&demon);
        locations[innerCave.GetId()].AddMonster(&dragon);
        locations[throneRoom.GetId()].AddMonster(&king);
        
    }

    vector<Node> AdventureGameMap::GetLocations()
    {
        return locations;
    }

}