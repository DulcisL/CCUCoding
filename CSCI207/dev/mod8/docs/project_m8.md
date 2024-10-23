# Module 7 - Blackjack Introduction

## Project Introduction

Who uses CMake? It is used by many development teams such as [QT development](https://www.qt.io/) and [Android app development](https://developer.android.com/). This is why it, along with Unit Testing, are critical to understand so you can put yourself ahead of others competing for a job. Usually, you will use g++ or clang to compile your code in CMake. You can even use CMake with [Visual Studio](https://learn.microsoft.com/en-us/cpp/build/cmake-projects-in-visual-studio?view=msvc-170) in a Windows environment.

We will also start using markdown on all projects going forward to create a readme.md file. [Markdown](https://www.markdownguide.org/cheat-sheet/) is the go-to environment for developers to convay information usually to other developers. This includes how to setup the project, what the project should accomplish, and anything else they feel is important to know about the project.

So, that being said, the purpose of this lab is to learn a little bit about CMake and why use it. Also, we will start learning about c++ classes, why use object oriented programming, and how to compile a class with into your executable.

## Setup:

1.	```
    cmake -S . -B build
    cmake --build build
    ```

## Todo:

-   creating a Deck class where you will include the deck creation, shuffle, and deal functions and create a DeckTest.cpp file to test that.
-   Private propery of Vector<Card> Deck
-   Private functions of buildDeck, shuffle(), 
-   Public functions of Deal()
-   Deal 4 cards

* buildDeck () - constructs a 52 card deck
* Shuffle() - randomizes the vector
* Deal() - Returns a single card and removes it from the deck

## Project Instructions


### Project Details



## Deliverables

-   Zip up the entire working directory and drop in this weeks Moodle project dropbox.