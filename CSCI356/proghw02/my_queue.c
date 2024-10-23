/*
 * my_queue.c - queue functions for my_queue.h prototypes
 *
 * Author: Lakota Dolce
 *
 * Course: CSCI 356
 * Version 1.0
 */

#include <stdio.h>
#include <stdlib.h>
#include "my_queue.h"

// Creates a queue
// Returns: a pointer to a queue
queue newqueue() {
    queue q = (queue) malloc(sizeof(struct queueS));
    // Initialize to NULL
    q->front = NULL;
    q->rear = NULL;  
    return q;
}

/*
 * checks the status of a queue
 * queue q: a queue to check for emptiness; q must not be NULL
 * returns: value is > 0 iff queue has no elements
 */
int isempty(const queue q) {
    return (q->front == NULL);
}

/*
 * adds item to end of queue
 * queue q: 	a queue to append; q must not be NULL
 * void* item:	a pointer to an item to be enqueued onto queue
 * returns:		item appended to queue
 */
void enqueue(queue q, void* item) {
    q_element new_element = (q_element) malloc(sizeof(struct q_elementS));
    new_element->contents = item;
    new_element->next = NULL;

    if (isempty(q)) {
        q->front = new_element;
        // Set rear when queue is empty
        q->rear = new_element;
    } else {
        // Link new element to the end
        q->rear->next = new_element;
        // Update rear pointer  
        q->rear = new_element;          
    }
}

/*
 * dequeues first item from queue
 * queue q: a queue to remove an item: q must not be NULL
 * returns: item returned was front of queue and next element
 * 			is new head of queue
 */
void* dequeue(queue q) {
    if (isempty(q)) {
        printf("Queue is empty.\n");
        return NULL;
    }

    q_element temp = q->front;
    void* item = temp->contents;
    q->front = temp->next;

    // If the queue is now empty
    if (q->front == NULL) {
        // Update rear to NULL  
        q->rear = NULL;      
    }

    free(temp);
    return item;
}

/*
 * allows fo first item from queue to be examined
 * queue q: a queue to check: q must not be NULL
 * returns: item returned is current front of queue and
 * 			queue is left unaltered
 */
void* peek(queue q) {
    if (isempty(q)) {
        printf("Queue is empty.\n");
        return NULL;
    }
    return q->front->contents;
}

// Frees all elements in the queue
// queue q: a queue to free; q must not be NULL
void free_queue(queue q) {
    while (!isempty(q)) {
        dequeue(q);
    }
    free(q);  // Free the queue structure itself
}
