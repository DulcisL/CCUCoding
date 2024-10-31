add_executable(
    blackjacktests
    BlackjackTest.cpp
)

target_link_libraries(
    blackjacktests
    GTest::gtest_main
    CardLib
)