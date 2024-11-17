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
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/wait.h>
#include <errno.h>

// Function prototypes
char* WarGames(int card1, int card2);
int CardSelection();
int SuitSelection();
char* ToString(int cardValue, int suitValue);
void ChildProcess(char* socket_path);
void PlayRound(int sockfd, int* roundCount, int* winCount1, int* winCount2, int* tieCount, pid_t CID1, pid_t CID2);

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
    //If totalRounds is negative abort
    if (totalRounds <= 0) {
        fprintf(stderr, "Error: The number of rounds must be a positive integer.\n");
        exit(EXIT_FAILURE);
    }
    printf("-----Welcome to the War Tournament-----\n");
    // Initialize
    pid_t CID1, CID2;
    int roundCount = 0, winCount1 = 0, winCount2 = 0, tieCount = 0;
    char result[25];
    struct sockaddr_un serv_addr;
    int sockfd, c1, c2, size, binded, listening;
    char* socket_path = "WarTournament";
    printf("Tournament has been initialized\n");

    // Clear socket if existing still
    if (unlink(socket_path) == -1 && errno != ENOENT) {
        perror("Error removing old socket file");
        exit(EXIT_FAILURE);
    }
    printf("Old socket file cleared if existed\n");
    
    //Create Socket
    sockfd = socket(AF_UNIX, SOCK_STREAM, 0);

    //Check if Socket was successful
    if (sockfd < 0){
        perror("Socket error\n");
        unlink(socket_path);
        exit(EXIT_FAILURE);
    }

    // Set up socket
    serv_addr.sun_family = AF_UNIX;
    strcpy(serv_addr.sun_path, socket_path);
    printf("socket path created\n");
    //Clear socket
    unlink(socket_path);
    printf("socket path cleared\n");

    //Bind to server socket
    size = sizeof(serv_addr);
    binded = bind(sockfd, (struct sockaddr *) &serv_addr, size);
    if( binded < 0){
        perror("Bind error occurred\n");
        unlink(socket_path);
        exit(EXIT_FAILURE);
    }
    printf("socket bound %d\n", binded);

    //Check for listening
    listening = listen(sockfd, 5);
    if(listening < 0){
        perror("Listen error\n");
        unlink(socket_path);
        exit(EXIT_FAILURE);
    }
    printf("Socket is listening with backlog of 5, %d\n", listening);

    // Allow server socket setup to finalize
    printf("Server socket ready, forking children...\n");
    sleep(1); 

    // Set up child processes
    CID1 = fork();
    //Check if fork was a success
    if (CID1 == -1) {
        perror("Fork Failed");
        unlink(socket_path);
        exit(EXIT_FAILURE);
    }
    if (CID1 > 0) {

    }
    else {
        //Call childprocess
        ChildProcess(socket_path);
        //Exit gracefully
        exit(0);
    }

    //Repeat above for child 2
    CID2 = fork();
    if (CID2 == -1) {
        perror("Fork Failed");
        unlink(socket_path);
        exit(EXIT_FAILURE);
    }
    if (CID2 > 0) {

    }
    else {
        ChildProcess(socket_path);
        exit(0);
    }

    //Accept connection
    c1 = accept(sockfd, NULL, NULL);
    printf("%d\n", c1);
    if(c1 < -1){
        perror("Accept error\n");
        unlink(socket_path);
        exit(EXIT_FAILURE);
    }
    printf("Connection to contestant 1 is good\n");

    //Repeat for connection 2
    c2 = accept(sockfd, NULL, NULL);
    printf("%d\n", c2);
    if(c2 < -1){
        perror("Accept error\n");
        unlink(socket_path);
        exit(EXIT_FAILURE);
    }
    printf("Connection to contestant 2 is good\n");
    
    while (roundCount < totalRounds && totalRounds != 0) {
    PlayRound(c1, &roundCount, &winCount1, &winCount2, &tieCount, CID1, CID2);
    }

    // Handle sudden death if there's a tie
    while (winCount1 == winCount2) {
        printf("Welcome to sudden death\n");
        PlayRound(c1, &roundCount, &winCount1, &winCount2, &tieCount, CID1, CID2);
    }

    //print overall winner
    printf("Tournament Results\n");
    printf("------------------------------------------------\n\n");
    printf("Child 1 had %d wins, Child 2 had %d wins\n", winCount1, winCount2);
    printf("%s\n", WarGames(winCount1, winCount2));

    //Kill Children processes
    char* message = "EXIT";
    //Tell children to exit
    write(sockfd, message, strlen(message) + 1);

    //close socket
    close(sockfd);
    unlink(socket_path);
    exit(EXIT_SUCCESS);
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
PlayRound
Desc -> Holds the logic of playing a round and determining the outcome
Param -> int sockfd - socket connection
Param -> int roundcount - the current round number
Param -> int wincount1, wincount2 - the current wincounts of players
Param -> int tiecount - the count of ties
Param -> pid_t CID1, CID2, the child process ID's
Returns -> nothing
*/
void PlayRound(int sockfd, int* roundCount, int* winCount1, int* winCount2, int* tieCount, pid_t CID1, pid_t CID2) {
    char result[25], temp[25], temp2[25];
    int card1 = 0, card2 = 0, suit1 = 0, suit2 = 0;

    // Reset the result
    result[0] = '\0';

    // Message children to get a card
    char* message = "Get Card";
    write(sockfd, message, strlen(message) + 1);
    read(sockfd, temp, sizeof(temp));

    write(sockfd, message, strlen(message) + 1);
    read(sockfd, temp2, sizeof(temp2));

    // Convert card values to integers
    card1 = atoi(temp);
    card2 = atoi(temp2);

    // Play game logic
    strcpy(result, WarGames(card1, card2));

    // Handle ties
    if (strcmp(result, "It is a tie") == 0) {
        // Ask for suits
        result[0] = '\0';
        message = "Suit Up";

        write(sockfd, message, strlen(message) + 1);
        read(sockfd, temp, sizeof(temp));

        write(sockfd, message, strlen(message) + 1);
        read(sockfd, temp2, sizeof(temp2));

        suit1 = atoi(temp);
        suit2 = atoi(temp2);

        // Play game logic with suits
        strcpy(result, WarGames(suit1, suit2));
    }

    // Print preround results
    printf("Round %d Stats -> Child 1: %d win(s), Child 2: %d win(s), Ties: %d\n", *roundCount + 1, *winCount1, *winCount2, *tieCount);

    // Update counts based on results
    if (strcmp(result, "It is a tie") == 0) {
        (*tieCount)++;
    } else if (strcmp(result, "Child 1 wins") == 0) {
        (*winCount1)++;
    } else if (strcmp(result, "Child 2 wins") == 0) {
        (*winCount2)++;
    }

    // Print results
    printf("------------------------------------------------\n\n");
    printf("Child 1 (%d) submits %s \n", CID1, ToString(card1, suit1));
    printf("Child 2 (%d) submits %s \n", CID2, ToString(card2, suit2));
    printf("------------------------------------------------\n\n");
    printf("%s\n", result);
    printf("------------------------------------------------\n\n");

    (*roundCount)++;
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
void ChildProcess(char* socket_path) {
    //Initialize
    char message[25];
    int connect_check;
    struct sockaddr_un s_addr;
    int sockfd, c;

    //seed using the child pid
    srand(getpid());

    //Create Socket
    sockfd = socket(AF_UNIX, SOCK_STREAM, 0);

    //Check if Socket was successful
    if (sockfd < 0){
        perror("Socket error child");
    }

    //Set up socket address
    s_addr.sun_family = AF_UNIX;
    strcpy(s_addr.sun_path, socket_path);

    //Check connection to server
    for (int i = 0; i < 5; i++) {
    connect_check = connect(sockfd, (struct sockaddr *) &s_addr, sizeof(s_addr));
    if (connect_check == 0) {
        printf("Child %d connected successfully\n", getpid());
        break;
    }
    perror("Child connection unsuccessful, retrying...");
    sleep(1);
    }
    if (connect_check != 0) {
        perror("Child unable to connect after retries");
        exit(EXIT_FAILURE);
    }


    while (1) {
        int card = 0, suit = 0;
        //Read message
        read(sockfd, message, sizeof(message));

        //Check Message
        if (strcmp(message, "Get Card") == 0) {
            //get card
            card = CardSelection();
            char cardStr[10];
            //convert to string
            sprintf(cardStr, "%d", card);
            //return card
            write(sockfd, cardStr, strlen(cardStr) + 1);
            continue;
        }
        if (strcmp(message, "Suit Up") == 0) {
            //Get suit
            suit = SuitSelection();
            char suitStr[10];
            //convert to string
            sprintf(suitStr, "%d", suit);
            //return suit
            write(sockfd, suitStr, strlen(suitStr) + 1);
            continue;
        }
        if (strcmp(message, "EXIT") == 0) {
            //break loop to let process finish and kill it
            break;
        }
    }
    close(sockfd);
    unlink(socket_path);
    exit(EXIT_SUCCESS);
}
