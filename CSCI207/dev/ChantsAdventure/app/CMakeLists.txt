# set up executable
add_executable(ChantsAdventure game.cpp)

# add library that was add in the CMakeLists in the src dir to the executable
target_link_libraries(ChantsAdventure PRIVATE GameMap)
target_include_directories(ChantsAdventure PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}")