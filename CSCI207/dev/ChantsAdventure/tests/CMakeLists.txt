add_executable(
    adventuretests
    adventuretests.cpp
)

target_link_libraries(
    adventuretests
    GTest::gtest_main
    GameMap
)