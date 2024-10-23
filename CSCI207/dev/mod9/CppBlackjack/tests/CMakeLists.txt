add_executable(
    blackjacktests
    blackjacktest.cpp
)

target_link_libraries(
    blackjacktests
    GTest::gtest_main
    CardLib
)