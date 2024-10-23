/*
 * credit_rating.c - main functions used for the program
 *
 * Author: Lakota Dolce
 *
 *
 * Course: CSCI 356
 * Version 1.0
 */
//Any libraries needed
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

//Any Files needed
#include "my_queue.h"
#include "credit_rating.h"
 

/*ToString -> For printing the credit user and score
Struct -> credit_rating
Param -> struct of a user
Returns -> Printable string of credit user and score
*/
char* ToString(const struct credit_rating* rating) {
    static char buffer[50];
    //Return the string with the info in a readable formatted string
    sprintf(buffer, "User: %s Score: %i", rating->name, rating->score);
    return buffer;
}

/*clearBuffer -> clears input buffer to prevent reading the wrong thing between inputs
Struct -> None
Param -> None
Returns -> None
*/
void clearBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);  // Discards characters in the buffer
}

/*choiceOne -> completes choice one for user
Struct -> None
Param -> &storage - pass by reference the queue
Returns -> None
*/
void choiceOne(queue storage){
    //Initialize
    int check = 1;
    char name[25];
    int score;

    while (1){
        //Get the name for the credit rating
        while (check == 1){
            printf("What is the name of for the credit rating (25 characters or less, must hit enter 2x)? \n");
            fgets(name, sizeof(name), stdin);
            //clear buffer and remove new line
            name[strcspn(name, "\n")] = '\0';
            clearBuffer();

            if (strlen(name) >= 0) {
                check = 0;
            }
        }
        //Check for break condition
        if (strlen(name) == 0){
            break;
        }

        //reset check value
        check = 1;

        // get score
        while (check == 1){

            printf("What is the rating of for the credit rating (0 < score < 850)?\n");
            scanf(" %d", &score);
            //Clear input buffer
            clearBuffer();
            //Error Check
            if (score > 850 || score < 0){
                printf("The score is not valid please try again \n");
                continue;
            }
            else {
                check = 0;
            }
        }
        //reset check
        check = 1;

        //initialize the rating and make space for it
        struct credit_rating* rating = malloc(sizeof(struct credit_rating));
        //Make sure rating isn't null
        if (rating == NULL) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(EXIT_FAILURE);
        }

        // Set the rating attributes
        strcpy((*rating).name, name);
        (*rating).score = score;

        // Pass rating to the queue
        enqueue(storage, rating); 
        continue; //Restart the loop  
    }
    
}

/*choiceTwo -> completes choice two for user
Struct -> None
Param -> &storage - the queue passed by reference
Returns -> None
*/
void choiceTwo(queue storage){
    //Print out the queue 
    int count = 1;
    float average = 0;
    while (!isempty(storage)){
        //get rating from queue
        struct credit_rating* rated = dequeue(storage);
        //print 
        printf("Person %d: %s\n", count, ToString(rated));
        //add items to average
        average += (*rated).score;
        count += 1;
    }
    // divide by the count of item in queue
    average = average / (count - 1);
    //print average
    printf("The total average was %f \n", average);
}


/*main -> Print out the menu and call any functions needed for the user. 
Param -> None
Returns -> Integer for success or fail
*/

int main(){

    //Init loop and variables
    char choice = '0';
    queue storage;

    //initialize the queue
    storage = newqueue();

    while (choice != 5){
        //Get the menu and print out
        printf("\nWelcome to the credit rating and storage program\n");
        //Ask user what they want to do
        printf("Please choose from the following options: \n");
        printf("To input new scores please enter 1\n");
        printf("To print out the credit scores please enter 2\n");
        printf("To exit the program to please enter 5\n");
        //Take the user input and clear input buffer
        scanf(" %c", &choice);
        clearBuffer();

        //Check if choice is 5
        if (choice == '5'){
            //break the loop
            break;
        }
        //Error check the user input
        if (choice < '1' || choice > '3'){
            // Tell user there was an error
            printf("The input was outside of the available choices\n");
            printf("Please try again");
            continue; //Restart the loop
        }
        //Complete user wants
        if (choice == '1'){
            choiceOne(storage);
        }
            
            
        if (choice == '2'){
            choiceTwo(storage);
        }
    }

    return 0;
}