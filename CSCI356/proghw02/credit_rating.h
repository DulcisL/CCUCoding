/*
 * my_queue.h - header file for the prototype functions of credit_rating.c
 *
 * Author: Lakota Dolce
 *
 * Course: CSCI 356
 * Version 1.0
 */
// Make sure the credit_rating is defined
#ifndef CREDIT_RATING_H_
#define CREDIT_RATING_H_

// Included libraries
#include <stdlib.h>

struct credit_rating {
    // Person's name up to 25 characters
    char name[25];
    // Person's score
    int score;
};

// Function prototype for ToString
// Takes a pointer to a credit_rating struct and returns a string representation of it
char* ToString(const struct credit_rating* rating);

#endif /* CREDIT_RATING_H_ */
