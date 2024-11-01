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

/** FindWinners
* @desc: A function to determine who wins and loses
* @param - vector<Player> Players - a vector storing the players in the game
* @return - none
*/
void FindWinners(vector<Player>& players);

/** DealCards
* @desc: A function to deal cards to the players
* @param - vector<Player> Players - a vector storing the players in the game
* @param - vector<Deck> deck - a vector containing the cards in play
* @return - none
*/
void DealCards(Player& player, vector<Deck>& deck);

/** TieBreaker
* @desc: A function to determine who wins in a tie against the dealer
* @param - Player player - A player instance
* @param - Player dealer - The dealer
* @return - none
*/
void TieBreaker(Player& player, Player& dealer);

/** Score
* @desc: A function to determine check if the player has an ace after bust condition
* @param - Player player - A player instance
* @return - none
*/
int Score(Player& player);

/** Results
* @desc: A function to print the results of the game
* @param vector<Player> players - a vector storing the players
* @param int numDecks - the number of decks used in the game
* @return int numAces - The number of aces held by the player
*/
void Results(vector<Player> players, int numDecks);

/** PlayerSetup
* @desc: A function to set up the players for the game
* @param vector<Player> players - a vector to store players
* @return int numDecks - the number of decks needed
*/
int PlayerSetup(vector<Player> &players);

/** Main
* @desc: The main function of the Blackjack game
* @param - none
* @return - int for success
*/
int main(){
    //Initialize variables
    bool quit = false;
    vector <Player> players;
    //Seed rand
    srand(time(nullptr));

    //Set up loop for players to play rounds
    while (quit != true){
        int i = 0;
        int decksNeeded = 1;
        bool endRound;

        //Get players set up
        decksNeeded = PlayerSetup(players);
        //Set up the deck
        Deck deck(decksNeeded, true);

        //Deal opening hand of 2 cards
        int count = 0;
        while (count < 2){
            //Go through each player and deal a card then repeat
            for (Player& p: players){
                p.Deal(deck);
            }
            count ++; 
        }
        
        //play game
        //check for blackjack on deal
        for (Player& p: players){
            if (Score(p) == 21){
                //Check the dealer and end round if true
                if (p.GetName() == "Dealer"){
                    quit = true;
                }
                //Check for players 
                if (p.GetName() != "Dealer"){
                    //If players have blackjack on deal Wins else lose
                    p.Status = "Wins";
                }
                else{
                    p.Status = "Loses";
                }
            }
        }
        if (quit == true){
            //Check for round end due to blackjack on deal
            Results(players, decksNeeded);
            continue;
        }
        //Deal cards as players need them
        for (Player& p: players){
            //If score is less than 21 deal a card
            while (Score(p)  < 21 && Score(p) <= p.Threshold){
                p.Deal(deck);
            }
            //move on to next player
            continue;
        } 

        //Check for winners
        FindWinners(players); 

        //Print the results
        Results(players, decksNeeded);

        

        //Ask user if they would like to play another round
        char input;
        while (true){
            cout << "Would you like to play another round? (Y/N) " << endl;
            cin >> input;
            //Error check
            if (input == 'y' || input == 'Y'){
                //run the game again
                quit = false;
                //Clear the vector
                players.clear();
                break;
            }
            if (input == 'n' || input == 'N'){
                //end the game
                quit = true;
                break;
            }
            else {
                cout << "That was not a valid choice, please try again" << endl;
            }
        }
    }
    
    //Tell player goodbye
    cout << "Thanks for playing" << endl;
    return 0;
}

void FindWinners(vector<Player> &players){
    //Check for Wins or loses
    Player& dealer = players[players.size() - 1];
    int dealerScore = Score(dealer);
    for (Player& p: players){
        int playerScore = Score(p);

        //Don't need to do it for dealer
        if(p.GetName() == "Dealer"){
            continue;
        }
        //make sure dealer didn't bust or get 21
        if (dealerScore < 21){
            if (playerScore == 21){
                p.Status = "Wins";
                continue;
            }
            if (playerScore > 21){
                p.Status = "Busted";
                continue;
            }

            //Otherwise check against the dealer
            if (playerScore < dealerScore){
                p.Status = "Lost";
                continue;
            }
            if (playerScore >= dealerScore && playerScore <= 21){
                p.Status = "Wins";
                continue;
            }
        }
        //Check if dealer got 21
        if (dealerScore == 21){
            //If player doesn't have 21 lost
            if (playerScore < 21 || playerScore > 21){
                if (playerScore > 21){
                    p.Status = "Busted";
                }
                else {
                    p.Status = "Lost";
                }
                continue;
            }
            //If player ties dealer score then run tie breaker
            if (playerScore == 21){
                TieBreaker(p, dealer);
            }
        }
        //If Dealer busts
        if (dealerScore > 21){
            dealer.Status = "Busted";
            //If player didn't bust they win
            if (playerScore <= 21){
                p.Status = "Wins";
            }
            else{
                p.Status = "Busted";
            }
        }
    }
}

void TieBreaker(Player &player, Player &dealer){
    //get the number of cards in hand
    if (player.GetHand().size() <= dealer.GetHand().size()){
        player.Status = "Wins";
    }
    else {
        player.Status = "Lost";
    }
}

void Results(vector<Player> players, int numDecks){
    //Format the output
    cout << "\nNumber of Decks: " << numDecks << endl;
    cout << setw(25) << "Players" << setw(10) << "Score" << setw(15)<< "Wins/Loss" << setw(15) <<  "Hand" << endl;
    cout << "___________________________________________________________________________________________" << endl;
    for (int i = 0; i < players.size(); i++){
        //get the cards
        string temp;
        for (Card c: players[i].GetHand()){
            temp += c.ToString() + ", ";
        }
        //print the result
        cout << "* " << setw(5) << i + 1 << setw(15) << players[i].GetName() << setw(10) << Score(players[i]) << setw(20) << players[i].Status << " | "  << temp <<  endl;
    }
    cout << "___________________________________________________________________________________________" << endl;
}

int Score(Player& player){
    int numAces = 0;
    int totalScore = player.CalculateScore();
    for(Card& c: player.GetHand()){
        if (c.GetValue() == 11){
            numAces += 1;
        }
    }
    while (player.CalculateScore() > 21 && numAces > 0){
        numAces -= 1;
        totalScore -= 10;
    }
    return totalScore;
}

int PlayerSetup(vector<Player> &players){
    //initialize
    int numPlayers = 0;
    int numDecks = 0;
    string temp;

    //Get number of players
    //Set up loop to error check
    while (true){
        cout << "How many players do you want in the game? " << endl;
        cin >> temp;
        //convert to an int
        try{
            numPlayers = stoi(temp);
            if (numPlayers > 0){
                break;
            }
            else{
                throw -1;
            }
        }
        //catchinvalid inputs
        catch(...){
            cout << temp << " was not a valid number (number must be > 0), please try again" << endl;
            cin.clear();
        }
        
    }

    //Add a spot for the dealer
    numPlayers += 1;

    //account for more than 7 players players
    numDecks = ceil(numPlayers / 7.0);

    //Get players set up
    int i = 0;
    while (i < numPlayers){
        //initialize temp vars
        int threshold;
        string playerName = "";
        //get all the players
        if (i < numPlayers - 1){
            
            while(true){
                //Get name
                cout << "What is the name of player "<< (i + 1) << "?" << endl;\
                cin.clear();
                std::getline(std::cin, playerName);

                //Check if a name was entered
                if (playerName.size() <= 0){
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
    return numDecks;
}
