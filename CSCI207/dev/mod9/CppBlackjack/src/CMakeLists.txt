#create a link library out of all the classes
add_library(CardLib STATIC
        Card.cpp
        Deck.cpp
        Player.cpp)

target_include_directories(CardLib PUBLIC "${CMAKE_CURRENT_SOURCE_DIR}")