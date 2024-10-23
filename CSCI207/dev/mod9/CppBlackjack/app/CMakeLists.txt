# name the executable and list the main file (Game.cpp in this case)
add_executable(BlackJack Game.cpp)

# all the .cpp files in src folder will compile to a linked library, in this case called CardLib (see src folder)
target_link_libraries(BlackJack PUBLIC CardLib)
target_include_directories(BlackJack PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}")