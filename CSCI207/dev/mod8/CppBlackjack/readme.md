# CPP Blackjack project
## Description:

This project is to build a game of blackjack that can be played. 
### Summary
- Card.cpp is used to store the card object along with it's functions.

- Card.h is the header file for the Card object. 

- CardTest.cpp is used to test the card object and new functions and objects to be added in the future.


## Build:
* *Note* to build this project you need to have cmake version 3.14
* Use `cmake -S . -B build` and `cmake --build build` to build the file the first time then you only need `cmake --build build` to change the build after that.


# Constraints: 
## Problems:

* *resolved* - see solutions 1/2) - When shuffling the deck, 2 random indices did not work
* *resolved* - see solutions 3)- When dealing skips every other card (forward or reverse)
* *resolved* - see solutions 4)- Deck doesn't change size when using `pop_back()` or `erase()` functions / Deck doesn't remove items when using the above functions
* When incrementing backwards card.cpp ToString sometimes prints weird (such as prints the status of isFaceUp)

## Solutions:

1) Shuffling the deck doesn't like using two random indices so 1 is used along with the index using i
2) Keeping the randint and shuffle within deck size use modulo of deck size
3) Instead of using an index for the deal function using the `deck.back()` function skips to the back automatically. (due to `pop_back()` as causing the skip as it didn't account for the removed card) (also fixed incrementing backwards to print the card)
4) To deal the deck had to be passed by reference and not by value otherwise just made a copy and did not save to the original deck

## Sources:

* GeeksforGeeks
* Reddit
* StackOverflow
* ChatGPT
* Google / Google AI overview