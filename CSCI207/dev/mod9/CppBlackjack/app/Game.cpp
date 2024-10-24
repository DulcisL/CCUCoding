/**
 * @file Game.cpp
 * @author Lakota Dolce
 * @brief This is the main file for the Blackjack game
 * @version 0.1
 * @date 2024-09-25
 *
 */

#include <vector>
#include <string.h>
#include <stdexcept>
#include <iostream>

main(){
    //Initialize variables
    bool quit = false;
    srand(time(nullptr));
    vector <Player> players;

    //Set up loop for players to play rounds
    while (quit != true){
        int numPlayers = 0;
        int i = 0;

        //Get number of players
        cout << "How many players do you want in the game?" << endl;
        getline(cin, numPlayers);

        //Get players
        while (i < numPlayers + 1){
            int threshold;
            string playerName;
            Player player;

            if (i < playerName){
                //Get name
                cout << "What is the name of player %i? \n";
                getline(cin, playerName);

                //Get threshold for player
                //get rand number %2  for threshold
                int randInt = rand() %2;
                if (randInt == 0){
                    //make player more aggressive
                    threshold = 17;
                }
                if (randInt == 1){
                    //make player more conservative
                    threshold = 12;
                }
            }
            //Add Dealer
            if (i < numPlayers){
                //Add dealer
                playerName = "Dealer";
                //Dealer has a threshold of 17 always
                threshold = 17
            }
            players.push_back(player(playerName, threshold));
        }

        //Deal opening hand

        //play game
            //check for black jack on first hand with dealer

        //print the results

        //Ask user if they would like to play another round
    }
    
    //Tell player goodbye
    cout << "Thanks for playing" << endl;
}