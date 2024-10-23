/*
    Name:
    Class:
    Project:
    Last Date:
*/
#include <iostream>
#include <ctime>
using namespace std;

/// @brief
/// @param argc the number of arguments passed into main
/// @param argv the list of arguments passed into main
/// @return integer code indicating success or not
int main(int argc, char *argv[])
{
    // note that without seeding the random number generator you will get the same random numbers every time
    int random_value_no_seed = rand() % 101; // Generate a random number between 0 and 100
    cout << random_value_no_seed << endl;

    // uncomment the code below after running this code several times
    // srand(time(nullptr)); // use current time as seed for random generator
    // int random_value = rand() % 101;
    // cout << random_value << endl;

    int lowerBound = 20, upperBound = 100;
    // This program will create some sequence of random
    // numbers on every program run within range lb to ub
    for (int i = 0; i < 50; i++)
        cout << (rand() % (upperBound - lowerBound + 1)) + lowerBound << " ";

    return 0;
}