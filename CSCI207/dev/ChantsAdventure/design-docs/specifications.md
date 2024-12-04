# Specifications for Chants Adventure

## Game Description

Chanticleer's Adventure Game is a single player text-based adventure game. The object of the game is to defeat the king. The player moves through the game by issuing text commands such as west, take hammer, or drop staff. After each movement, the game will respond by telling the player where she is currently located by describing her surroundings. Each location may have several paths in any number of directions. Each location may contain objects of interest. Along the way, the player can pick up items that will help fight enemies, and work towards defeating the king. The game can be saved and opened at the same location and game parameters.

## Game parameters are:

-	Player starts with health worth 12,500 points
-	Player gain or lose points depending on the events that happen during the game
-	Player loses the game if they die

## Game objects of interest:

-	Player – Chants Adventure is a single player game

-	Benightedness - world

-	Path – paths may be bidirectional or only one direction

-	Location – points on the map

-	Directions - node number or name

-	Assets – help or hurt the player depending on the item

-	Demon - A demon, beware of deals
-   Wolves - Wild animals found all over, generally agressive, watch out for packs fo them.
-	Dwarves – creatures of the cave obsessed with shiny objects, don't take kindly to trespassers. 
-   Dragons - Hoarder of treasure, Generally found in caves when not in the air.
-	Knight – Guards of the castle 
-	King – Malicious ruler of the lands of 

## List of actions (use: verb + noun) examples:

-	Walk, Take, Drop, Examine, Read, Push, Pull, Kick, Spray, Sit, Stand
-	Inventory (used to show list of items a player holds)

## Game Objects

	Game objects all have a value in points. All game objects may be picked up. All objects can be be used in combat, however all may not have an effective use and may just be wasted. The player may pick up an object and drop it at another location in the game.

## Possible list of objects

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

## Possible Game Map Locations (Flushed out during storyboarding)

-   Dark Room
-   Meadow
-   Forest
-   Abandoned Farm
-   Mountain Pass
-   Cave
-   Inner Cave
-   Abandoned House
-   Abandoned City
-   Riverside
-   Path
-   Fork
-   City
-   Trader Shop
-   Jail
-   Castle
-   Castle Cellar
-   Castle Kitchen
-   Throne Room Doors
-   Throne Room

## Objectives

-	Action Adventure Game Engine Design 
-	Game object design and implementation techniques
-	Tools
    -	UMLet
    -   TDD (unit testing using gtest)
    -   Doxygen


In the tradition of the original Zork text based adventure game, this course teaches design methodologies for building text based action adventure game engine designs. It concentrates on object oriented strategies and using agile software development methods. By the end of class the student will be familiar with:

-	UML
-	C++
-   CMake
-	Object Oriented Design (OOD) and object communication
-	Design patterns
-	Source control
-	Unit testing procedures
-   Documentation
-   Markdown
