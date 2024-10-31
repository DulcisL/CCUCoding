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
#include <math.h>

/** Blackjack
* @desc: The main function of the Blackjack game
* @param - none
* @return - none
*/
void Blackjack(){
    //Initialize variables
    bool quit = false;
    vector <Player> players;
    //Seed rand
    srand(time(nullptr));

    //Set up loop for players to play rounds
    while (quit != true){
        int numPlayers;
        string temp;
        int i = 0;
        float decksNeeded = 0;
        bool endRound;

        //Set up loop to error check
        while (true){
            //Get number of players
            cout << "How many players do you want in the game? (must be less than 7)" << endl;
            cin >> temp;
            //convert to an int
            numPlayers = stoi(temp);
            if (numPlayers > 0){
                if (numPlayers > 7){
                    cout << "Can't have that many players in a game, please try again." << endl;
                    continue;
                }
                else {
                    break;
                }
            }
            else{
                cout << "That was not a valid number please try again" << endl;
                cin.clear();
            }
        }
        
        //Add a spot for the dealer
        numPlayers += 1;
       cout << numPlayers << endl;
        //account for more than 7 players players
        decksNeeded = ceil(numPlayers / 7.0);
        cout << decksNeeded << endl;

        //Set up the deck
        Deck deck(decksNeeded);

        //Get players set up
        while (i < numPlayers){
            //initialize temp vars
            int threshold;
            string playerName = "";
            //get all the players
            if (i < numPlayers - 1){
                
                while(true){
                    //Get GetName
                    cout << "What is the name of player "<< (i + 1) << "?" << endl;\
                    cin.clear();
                    cin >> playerName;

                    //Check if a name was entered
                    if (playerName.size() <=0){
                        cout << "That was not a valid input" << endl;
                        continue;
                    }
                    else {
                        break;
                    }
                }

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
            else{
                //Add dealer
                playerName = "Dealer";
                //Dealer has a threshold of 17
                threshold = 17;
            }
            //make the player
            players.push_back(Player(playerName, threshold));
            i += 1;
        }

        //Deal opening hand of 2 cards
        int count = 0;
        while (count < 2){
            //Go through each player and deal a card then repeat
            for (Player p: players){
                Card card = deck.deal();
                p.Deal(card);
            } 
            count ++; 
        }

        cout << "The openning hand was dealt" << endl;
        for (Player p: players){
            p.ToString();
        }
        
        //play game
        //check for black jack on deal
        for (Player p: players){
            if (p.CalculateScore() == 21){
                //Check the dealer and end round if true
                if (p.GetName() == "Dealer"){
                    quit = true;
                }
                //Check for players 
                if (p.GetName() != "Dealer"){
                    //If players have blackjack on deal Wins else lose
                    p.status = "Wins";
                }
            }
        }
        if (quit == true){
            //Check for round end
            continue;
        }
        //Deal cards as players need them
        for (Player p: players){
            //If score is less than 21 deal a card
            while (p.CalculateScore() < 21 && p.CalculateScore() <= p.threshold){
                Card card = deck.deal();
                p.Deal(card);
            }
            //move on to next player
            continue;
        }  

        //Check for Wins or loses
        Player dealer = players[players.size() - 1];
        for (i == 0; i < (players.size() - 1); i++){
            Player player = players[i];

            //make sure dealer didn't bust or get 21
            if (dealer.CalculateScore() < 21){
                if (player.CalculateScore() == 21){
                    player.status = "Wins";
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

/** main
* @desc: The main function
* @param - none
* @return - none
*/
int main(){
    //Call the function to play blackjack
    Blackjack();
    return 0;
}