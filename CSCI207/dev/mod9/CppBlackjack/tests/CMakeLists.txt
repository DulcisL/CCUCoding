add_executable(
    blackjacktests
    Blackjacktest.cpp
)

target_link_libraries(
    blackjacktests
    GTest::gtest_main
    CardLib
)