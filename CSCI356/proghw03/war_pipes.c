/*
Lakota Dolce
ProgHW03 - war_pipes.c
October 10, 2024
Dr. Fuchs
*/

//Included libraries
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

//Included files

//Function prototypes
char* WarGames;
int CardSelection;
int SuitSelction;
char* ToString;
void Pipes;
char* PassMessage;


/*
main
Desc -> main function of the program used to complete basic tasks and call other functions
Params -> none
Returns -> int for success
*/
int main (){
    //Initialize
    //Set up child processes
    //Seperate child processes by 1 second
    //Set up Pipes
    //Play game

}

/*
WarGames
Desc -> Contains the code to play war
Params -> CID1, CID2: Hold the child IDs 
Returns -> string result: result of who won
*/
char* WarGames (int CID1, int CID2){
    //Initialize
    char result[15];
    int card1 = PassMessage("New Card", CID1);
    int card2 = PassMessage("New Card", CID2);
    int suit1 = 0;
    int suit2 = 0;
    
    while (1){
        //print out the cards
        printf("Child1 submits %s **** Child2 submits %s",ToString(card1, suit1), ToString(card2, suit2));

        //Game logic
        if (card1 > card2){
            strcat(result, "Child1 wins\n");
            break;
        }
        if (card2 > card1){
            strcat(result, "Child2 wins\n");
            break;
        }
        if (card1 == card2){
            //ask for a suit
            int suit1 = PassMessage("suit up", CID1);
            int suit2 = PassMessage("suit up", CID2);

            if (suit1 > suit2){
                strcat(result, "Child1 wins\n");
                break;
            }
            if (suit2 > suit1){
                strcat(result, "Child2 wins\n");
                break;
            }
            if (suit1 == suit2){
                //Get new cards
                card1 = PassMessage("New Card", CID1);
                card2 = PassMessage("New Card", CID2);
                continue;
            }
        }

    }
    

    return result;
}

/*
CardSelection
Desc -> Randomly selects a card between value 1 and 14
Params -> None
Returns -> int cardValue: The value of the card 1-14
*/
int CardSelection(){
    //Initialize
    int cardValue;
    int timeNow;

    //Make sure that it is not the same time as previously
    timeNow = time(NULL);
    while ((timeNow + 2) > time(NULL)){
        continue;
    }

    //seed random generator with time pointer
    srand(time(NULL));

    //Get card value
    while (1){
        cardValue = rand() %14;
        //Check value is within 2 and 14
        if (cardValue >= 2 && cardValue <= 14){
            break;
        }
        //else reroll number
        continue;
    }
    
    //return value
    return cardValue;
}

/*
SuitSelection
Desc -> Randomly selects a suit between value 1 and 4
Params -> None
Returns -> in suitValue: The value of the suit 1-4
*/
int SuitSelection(){
    //Initialize
    int suitValue;
    int timeNow;

    //Make sure that it is not the same time as previously
    timeNow = time(NULL);
    while ((timeNow + 2) > time(NULL)){
        continue;
    }

    //seed random generator with time pointer
    srand(time(NULL));

    //Get card value
    while (1){
        suitValue = rand() %4;
        //Check value is within 1 and 4
        if (suitValue >= 1 && suitValue <= 4){
            break;
        }
        //else reroll number
        continue;
    }
    
    //return value
    return suitValue;
}

/*
ToString
Desc -> Prints Out the card in a readable format
Params -> cardValue, suitValue: Holds the values for the card and suit
Returns -> char* stringedCard: Contains the desc of the card
*/
ToString(int cardValue, int suitValue){
    //Initialize
    char cardRead[30];
    
    //check if value is greater than 10 for royals
    if (cardValue > 10){
        switch (cardValue){
            case 11: strcat(cardRead, "Jack");
            case 12: strcat(cardRead, "Queen");
            case 13: strcat(cardRead, "King");
            case 14: strcat(cardRead, "Ace");
        }

    }
    if (cardValue <= 10) {
        //set to the face value
        strcat(cardRead, cardValue);
    }
    //check if suitValue exists
    if (suitValue == 0){
        //if not return the card
        return cardRead;
    }
    //If suit value then return card
    if (suitValue !=0){
        switch (suitValue){
            //order of suits in terms of power (based on game bridge)
            case 1: strcat(cardRead, "Clubs");
            case 2: strcat(cardRead, "Diamonds");
            case 3: strcat(cardRead, "Hearts");
            case 4: strcat(cardRead, "Spades");
        }
        return cardRead;
    }
}

/*
Pipe
Desc -> The basic pipe structure for message passing
Params ->
Returns ->
*/
void Pipe(){

}

/*
PassMessage
Desc -> Takes a message and sends to appropriate person
Param -> char* message: Holds the message to be passed
Param -> int CID: the child ID to be messaged
Returns -> char* response: the response of the child
*/
char* PassMessage(char* message, int CID){

}