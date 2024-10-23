/*
Lakota Dolce
ProgHW03 - war_pipes.c
October 10, 2024
Dr. Fuchs
*/
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

// Function prototypes
char* WarGames(int card1, int card2);
int CardSelection();
int SuitSelection();
char* ToString(int cardValue, int suitValue);
void ChildProcess(int childToParent[], int parentToChild[]);

/*
main
Desc -> main function of the program used to complete basic tasks and call other functions
Params -> int totalRounds - the desired number of rounds in the tournament
Returns -> int for success or failure
*/
int main(int argc, char *argv[]) {
    //if no total rounds supplied abort
    if (argc < 2){
        fprintf(stderr, "No argument given %s\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    int totalRounds = atoi(argv[1]);
    if (totalRounds <= 0) {
        fprintf(stderr, "Error: The number of rounds must be a positive integer.\n");
        exit(EXIT_FAILURE);
    }
    // Initialize
    pid_t CID1, CID2;
    int roundCount = 0, winCount1 = 0, winCount2 = 0, tieCount = 0;
    char result[25];

    // Set up Pipes
    int parentToChild1[2], childToParent1[2], parentToChild2[2], childToParent2[2];

    //Check if pipe was successful
    if (pipe(parentToChild1) == -1 || pipe(childToParent1) == -1 || pipe(parentToChild2) == -1 || pipe(childToParent2) == -1) {
        perror("pipe");
        return 1;
    }

    // Set up child processes
    CID1 = fork();
    //Check if fork was a success
    if (CID1 == -1) {
        perror("Fork Failed");
        exit(EXIT_FAILURE);
    }
    if (CID1 > 0) {
        close(parentToChild1[0]);  // Parent write only
        close(childToParent1[1]);  // Child read only
    } else {
        close(parentToChild1[1]);  // Parent write only
        close(childToParent1[0]);  // Child read only
        //Call childprocess
        ChildProcess(childToParent1, parentToChild1);
        //Kill process
        exit(0);
    }

    //repeat above for child 2
    CID2 = fork();
    if (CID2 == -1) {
        perror("Fork Failed");
        exit(EXIT_FAILURE);
    }
    if (CID2 > 0) {
        close(parentToChild2[0]);
        close(childToParent2[1]);
    } else {
        close(parentToChild2[1]);
        close(childToParent2[0]);
        ChildProcess(childToParent2, parentToChild2);
        exit(0);
    }

    while (roundCount <= totalRounds && totalRounds != 0) {
        //set default values
        int card1 = 0, card2 = 0, suit1 = 0, suit2 = 0;
        char temp[25], temp2[25];
    
        //Reset the result
        result[0] = '\0';
        // Write to child to send card
        char* message = "Get Card";
        write(parentToChild1[1], message, strlen(message) + 1);
        write(parentToChild2[1], message, strlen(message) + 1);

        // Read from child to get card
        read(childToParent1[0], temp, sizeof(temp));
        card1 = atoi(temp);
        read(childToParent2[0], temp2, sizeof(temp2));
        card2 = atoi(temp2);

        // Play game
        strcpy(result, WarGames(card1, card2));

        if (strcmp(result, "It is a tie") == 0) {
            //Reset the strings to null
            result[0] = '\0';
            char temp[25], temp2[25];

            //Ask for suit
            char* message = "Suit Up";
            write(parentToChild1[1], message, strlen(message) + 1);
            write(parentToChild2[1], message, strlen(message) + 1);
            //Get suit
            read(childToParent1[0], temp, sizeof(temp));
            //Convert to int
            suit1 = atoi(temp);
            read(childToParent2[0], temp2, sizeof(temp2));
            suit2 = atoi(temp2);
            //Call game logic
            strcpy(result, WarGames(suit1, suit2));
            
        }
        //print preround results
        printf("Round %d Stats -> Child 1: %d wins Child 2: %d wins Ties: %d \n", roundCount + 1, winCount1, winCount2, tieCount);
        
        //check and store results
        if (strcmp(result, "It is a tie") == 0){
            tieCount +=1;
        }
        if (strcmp(result, "Child 1 wins") == 0){
            winCount1 += 1;
        }
        if (strcmp(result, "Child 2 wins") == 0){
            winCount2 += 1;
        }
        roundCount +=1;

        //Print results
        printf("------------------------------------------------\n\n");
        printf("Child 1 (%d) submits %s \n", CID1, ToString(card1, suit1));
        printf("Child 2 (%d) submits %s \n", CID2, ToString(card2, suit2));
        printf("------------------------------------------------\n\n");
        printf("%s \n", result);
        printf("------------------------------------------------\n\n");
    }
    //print overall winner
    printf("Child 1 had %d wins, Child 2 had %d wins\n",winCount1, winCount2);
    printf("The grand winner is %s \n", WarGames(winCount1, winCount2));

    // Kill Children processes
    char* message = "EXIT";
    write(parentToChild1[1], message, strlen(message) + 1);
    write(parentToChild2[1], message, strlen(message) + 1);
}

/*
WarGames
Desc -> Contains the code to play war
Params -> card1 , card2: Holds the value of the card
Returns -> string result: result of who won
*/
char* WarGames(int card1, int card2) {
    if (card1 > card2) {
        return "Child 1 wins";
    }
    if (card1 < card2) {
        return "Child 2 wins";
    }
    if (card1 == card2){
        return "It is a tie";
    }
    return "An error occurred";
}

/*
CardSelection
Desc -> Randomly selects a card between value 2 and 14
Params -> None
Returns -> int cardValue: The value of the card 2-14
*/
int CardSelection() {
    return (rand() % 13) + 2;  // Generate a card between 2 and 14
}

/*
SuitSelection
Desc -> Randomly selects a suit between value 1 and 4
Params -> None
Returns -> in suitValue: The value of the suit 1-4
*/
int SuitSelection() {
    return (rand() % 4) + 1;  // Generate a suit between 1 and 4
}

/*
ToString
Desc -> Prints Out the card in a readable format
Params -> cardValue, suitValue: Holds the values for the card and suit
Returns -> char* cardRead: Contains the desc of the card
*/
char* ToString(int cardValue, int suitValue) {
    //initialize
    static char cardRead[30];
    //error check
    if (cardValue != 0){
        if (cardValue > 10) {
        switch (cardValue) {
            //Royals
            case 11: strcpy(cardRead, "Jack"); break;
            case 12: strcpy(cardRead, "Queen"); break;
            case 13: strcpy(cardRead, "King"); break;
            case 14: strcpy(cardRead, "Ace"); break;
            }
        }
        else {
            //Otherwise use face value
            sprintf(cardRead, "%d", cardValue);
        }
    }
    if (suitValue != 0) {
        //Spades beats hearts which beats diamonds which beats clubs
        switch (suitValue) {
            case 1: strcat(cardRead, " of Clubs"); break;
            case 2: strcat(cardRead, " of Diamonds"); break;
            case 3: strcat(cardRead, " of Hearts"); break;
            case 4: strcat(cardRead, " of Spades"); break;
        }
    }
    return cardRead;
}

/*
ChildProcess
Desc -> The child process function
Params -> childToParent, parentToChild - Pipes for communication
Returns -> none
*/
void ChildProcess(int childToParent[], int parentToChild[]) {
    //Initialize
    char message[25];
    //seed using the child pid
    srand(getpid());

    while (1) {
        int card = 0, suit = 0;
        //Read message
        read(parentToChild[0], message, sizeof(message));

        //Check Message
        if (strcmp(message, "Get Card") == 0) {
            //get card
            card = CardSelection();
            char cardStr[10];
            //convert to string
            sprintf(cardStr, "%d", card);
            //return card
            write(childToParent[1], cardStr, sizeof(cardStr));
            continue;
        }
        if (strcmp(message, "Suit Up") == 0) {
            //Get suit
            suit = SuitSelection();
            char suitStr[10];
            //convert to string
            sprintf(suitStr, "%d", suit);
            //return suit
            write(childToParent[1], suitStr, sizeof(suitStr));
            continue;
        }
        if (strcmp(message, "EXIT") == 0) {
            //break loop to let process finish and kill it
            break;
        }
    }
}