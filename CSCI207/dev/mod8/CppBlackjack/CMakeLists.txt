# required to set the cmake version
cmake_minimum_required(VERSION 3.14)
# a project name is required
project(blackjack)

# usually it is a good idea to include the c++ standard that is used
# in our case, at least 14 is required for gtest (googletest) unit testing
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# creating the executable, the path to each cpp file is relitive to where this CMakeLists.txt file is located
add_executable(blackjack Card.cpp Deck.cpp DeckTest.cpp)