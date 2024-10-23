# Module 7 - Blackjack Introduction

## Project Introduction

Who uses CMake? It is used by many development teams such as [QT development](https://www.qt.io/) and [Android app development](https://developer.android.com/). This is why it, along with Unit Testing, are critical to understand so you can put yourself ahead of others competing for a job. Usually, you will use g++ or clang to compile your code in CMake. You can even use CMake with [Visual Studio](https://learn.microsoft.com/en-us/cpp/build/cmake-projects-in-visual-studio?view=msvc-170) in a Windows environment.

We will also start using markdown on all projects going forward to create a readme.md file. [Markdown](https://www.markdownguide.org/cheat-sheet/) is the go-to environment for developers to convay information usually to other developers. This includes how to setup the project, what the project should accomplish, and anything else they feel is important to know about the project.

So, that being said, the purpose of this lab is to learn a little bit about CMake and why use it. Also, we will start learning about c++ classes, why use object oriented programming, and how to compile a class with into your executable.

## Setup:

1.	Download Card.h and Card.cpp from Moodle 6 (I would also watch the videos in the docs folder)
2.	Create a folder - I would call it CppBlackjack
3.	Put the Card.h and Card.cpp into that folder
4.  Add a file to CppBlackjack called CardTest.cpp
5.	Add a file to CppBlackjack called CMakeList.txt
6.  Add a folder to CppBlackjack called "build"
7.  Add a file to CppBlackjack called readme.md

## Todo:

-   Look over the Card.h and Card.cpp, try to get familiar with how a typical class is constructed in C++. This will make more sense as we move through the Blackjack game project.
-   Open CMakeLists.txt and enter this code block (#sign is a comment in cmake files):
    ```
    # required to set the cmake version
    cmake_minimum_required(VERSION 3.14)
    # a project name is required
    project(blackjack)

    # usually it is a good idea to include the c++ standard that is used
    # in our case, at least 14 is required for gtest (googletest) unit testing
    set(CMAKE_CXX_STANDARD 14)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    # creating the executable, the path to each cpp file is relitive to where this CMakeLists.txt file is located
    add_executable(blackjack CardTest.cpp Card.cpp)
    ```
-   Open the CardTest file and enter the following:
    ```
    #include <iostream>
    #include <vector>
    #include "Card.h"
    using namespace std;

    int main()
    {
        Card card(1, 1, true);
        cout << card.ToString() << endl;
        return 0;
    }
    ```
-   Make sure you have saved everything
-   Open a terminal window and make sure the cursor is located in the root of the project folder, where the CMakeLists.txt file is located
-   Type to following to create a cmake project and compile into an executable
    ```
    cmake -S . -B build
    cmake --build build
    ```
-   Note that anytime you want to rebuild the prject all you need is `cmake --build build`
-   Note that also, anytime you want to start over with the project, delete everything in the build folder and re-enter the two lines of code above.
-   Open the build folder and you should see the file blackjack that is an executable
-   From the terminal window, enter
    `./build/blackjack`
-   This should run the executable.

## Project Instructions

Now that everything is set up, you can proceed with this weeks project. Do not go forward unless you are able to compile the existing code using CMake.

For this project you will create code in CardTest.cpp that will test some of the features of the Card class. You will use a vector in the standard template library to hold 52 cards. You should use the `push_back()` function to add Cards to the vector. You can access items in the vector just like an array e.g. deck[1]. There are lots of good resources on vectors online and in the book. Look at chapter 7 on arrays and vectors.

### Project Details

-   Create a function called `void CreateDeckOfCard(vector<Card> &deck)`
-   Use this function to add 52 playing cards representing a normal deck of card. Look at the Card class to help understand how to create cards with different suits (1 - 4) and different values (1 - 13).
-   After creating the vector of cards, create a function called `void ToString(vector<Card> deck)` that display the entire deck to make sure it looks correct.
-   Create another function called `void Shuffle(vector<Card> &deck)` that randomizes the deck of cards.
-   Then, display the deck of cards to make sure they actually got shuffled.
-   Lastly, deal 4 cards from the shuffled deck, face up, and display those four cards. 
    -   Note, when you deal a card from the deck, it should be removed from the vector so that is you check the vector size, unlike an array, it is actually reduced.
-   Include details of how you solved the algorithms and problems for this project in the readme file using markdown. Include any references that you used to assist you including Internet, textbook, colaboration with peers, etc.. You can use this document to help you with headings, links, and lists (ordered and unordered).

## Deliverables

-   Zip up the entire working directory and drop in this weeks Moodle project dropbox.