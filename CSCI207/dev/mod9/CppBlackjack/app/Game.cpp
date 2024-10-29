/**
 * @file Game.cpp
 * @author Lakota Dolce
 * @brief This is the main file for the Blackjack game
 * @version 0.1
 * @date 2024-09-25
 *
 */
#include "../inc/Player.h"
#include "../inc/Card.h"
#include "../inc/Deck.h"

#include <vector>
#include <string>
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
        int decksNeeded = 0;
        bool endRound;

        //Get number of players
        cout << "How many players do you want in the game?" << endl;
        getline(cin, numPlayers);

        //account for more than 7 players
        decksNeeded = ceil(numPlayers / 7);
        // make deck face down
        Deck deck(decksNeeded, false);
        //Add a spot for the dealer
        numPlayers += 1;

        //Get players
        while (i < numPlayers){
            int threshold;
            string playerName;
            Player player;

            if (i < numPlayers - 1){
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
            if (i <= numPlayers){
                //Add dealer
                playerName = "Dealer";
                //Dealer has a threshold of 17
                threshold = 17;
            }
            players.push_back(player(playerName, threshold));
        }

        //Deal opening hand of 2 cards
        int count = 1;
        while (count <= 2){
            //Go through each player and deal a card then repeat
            for (i == 0, i < sizeof(players), i++) {
                Player player = players[i];
                player.Deal();
            }  
        }
        
        //play game
        //check for black jack on deal
        for (i == 0, i < sizeof(players), i++){
            if (players[i].score == 21){
                //Check the dealer and end round if true
                if (players.[i].name() == "Dealer"){
                    quit = true;
                }
                //Check for players 
                if (players[i].name() != "Dealer"){
                    //If players have blackjack on deal win else lose
                    players[i].status() = "Win";
                }
            }
        }
        if (quit == true){
            //Check for round end
            continue;
        }
        //Deal cards as players need them
        for (i == 0, i < sizeof(players), i++){
            //If score is less than 21 deal a card
            while (players[i].score < 21 && player[i].score <= players[i].threshold()){
                players[i].Deal()
            }
            //move on to next player
            continue;
        }  

        //Check for win or lose
        for (i == 0, i < sizeof(players), i++){
            if (players[i].score() == 21){
                players[i].status == "Win";
            }
            if (players[i].score() > 21){
                players[i].status = "Busted";
            }
            //Otherwise check against the dealer
            if (players[i].score < 21 && i < sizeOf(players)){
                if (players[i].score < players[sizeOf(players)].score && players[sizeOf(players)].status() != "Busted"){
                    players[i].status() = "Loses";
                }
                if (players[i].score >= players[sizeOf(players)].score && players[i].status() != "Busted"){
                    players[i].status() = "Wins";
                }
            }
        }

        //print the results
        cout << setw(16) << "Players" << setw(5) << "Score" << setw(5)<< "Win/Loss" << endl;
        cout << "___________________________________________________" << endl;
        for (i == 0, i < sizeof(players), i++){
            cout << '*' << setw(15) << players[i].name() << setw(5) << players[i].score() << setw(5) << player[i].status() << endl;
        }

        //Ask user if they would like to play another round
        cout << "Would you like to play another round? (Y/N) " << endl;
        cin >> input;
        if (input == 'y' || input == 'Y'){
            //run the game again
            quit = false;
            continue;
        }
        if (input == 'n' || input == 'N'){
            //end the game
            quit == true;
            break;
        }
    }
    
    //Tell player goodbye
    cout << "Thanks for playing" << endl;
}