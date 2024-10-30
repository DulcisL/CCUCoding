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
#include <iomanip>
#include <fstream>
#include <cmath>


/** main
* @desc: The main game logic
* @param - none
* @return - none
*/
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
            //initialize temp vars
            int threshold;
            string playerGetName;

            if (i < numPlayers - 1){
                //Get GetName
                cout << "What is the GetName of player %i? \n";
                getline(cin, playerGetName);

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
            if (i == numPlayers){
                //Add dealer
                playerGetName = "Dealer";
                //Dealer has a threshold of 17
                threshold = 17;
            }
            //make the player
            players.push_back(Player(playerGetName, threshold));
            i += 1;
        }

        //Deal opening hand of 2 cards
        int count = 1;
        while (count <= 2){
            //Go through each player and deal a card then repeat
            for (i == 0; i < players.size(); i++) {
                Player player = players[i];
                player.Deal(deck);
            }  
        }
        
        //play game
        //check for black jack on deal
        for (i == 0; i < players.size(); i++){
            if (players[i].CalculateScore() == 21){
                //Check the dealer and end round if true
                if (players[i].GetName() == "Dealer"){
                    quit = true;
                }
                //Check for players 
                if (players[i].GetName() != "Dealer"){
                    //If players have blackjack on deal Wins else lose
                    players[i].status = "Wins";
                }
            }
        }
        if (quit == true){
            //Check for round end
            continue;
        }
        //Deal cards as players need them
        for (i == 0; i < players.size(); i++){
            //If score is less than 21 deal a card
            while (players[i].CalculateScore() < 21 && players[i].CalculateScore() <= players[i].threshold){
                players[i].Deal(deck);
            }
            //move on to next player
            continue;
        }  

        //Check for Wins or loses
        Player dealer = players[players.size()];
        for (i == 0; i < (players.size() - 1); i++){
            Player player = players[i];

            //make sure dealer didn't bust or get 21
            if (dealer.CalculateScore() < 21){
                if (player.CalculateScore() == 21){
                    player.status == "Wins";
                    continue;
                }
                if (player.CalculateScore() > 21){
                    player.status = "Busted";
                    continue;
                }
                //Otherwise check against the dealer
                if (player.CalculateScore() < dealer.CalculateScore()){
                    players[i].status = "Lost";
                    continue;
                }
                if (player.CalculateScore() >= dealer.CalculateScore() && player.CalculateScore() <= 21){
                    players[i].status = "Wins";
                    continue;
                }
            }
            //Check if dealer got 21
            if (dealer.CalculateScore() == 21){
                //If player doesn't have 21 lost
                if (player.CalculateScore() < 21 || player.CalculateScore() > 21){
                    if (player.CalculateScore() > 21){
                        player.status = "Busted";
                    }
                    else {
                        player.status = "Lost";
                    }
                    continue;
                }
                //If player ties dealer CalculateScore
                if (player.CalculateScore() == 21){
                    //get the number of cards in hand
                    if (player.GetHand().size() < dealer.GetHand().size()){
                        player.status = "Wins";
                        continue;
                    }
                    else {
                        player.status = "Lost";
                        continue;
                    }
                }
            }
            //If Dealer busts
            if (dealer.CalculateScore() > 21){
                //If player didn't bust they win
                if (player.CalculateScore() <= 21){
                    player.status = "Wins";
                }
                else{
                    player.status = "Busted";
                }
            }
        }

        //print the results
        cout << setw(16) << "Players" << setw(5) << "CalculateScore" << setw(5)<< "Wins/Loss" << endl;
        cout << "___________________________________________________" << endl;
        for (i = 0; i < players.size(); i++){
            cout << '*' << setw(15) << players[i].GetName() << setw(5) << players[i].CalculateScore() << setw(5) << players[i].status << endl;
        }

        //Ask user if they would like to play another round
        char input;
        while (true){
            cout << "Would you like to play another round? (Y/N) " << endl;
            cin >> input;
            //Error check
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
            else {
                cout << "That was not a valid choice, please try again" << endl;
            }
        }
    }
    
    //Tell player goodbye
    cout << "Thanks for playing" << endl;
}