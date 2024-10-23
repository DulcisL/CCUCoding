/*
    Name:
    Class:
    Project:
    Last Date:
*/
#include <iostream>
using namespace std;

/// @brief Use gdb to debug this application to figure out why
///         the output is unexpected (runtime bug)
/// @param argc the number of arguments passed into main
/// @param argv the list of arguments passed into main
/// @return integer code indicating success or not
int main(int argc, char *argv[])
{
    int arr[] = {1, 2, 3, 4, 5}; // array initialization
    const int MAX_NUMBER = sizeof(arr);
    int counter = 0;
    bool done = false;

    // There are three loops that are used more than others: for, while, and foreach

    // for loop
    cout << "Using a for loop:\n";
    for (int i = 0; i < MAX_NUMBER; i++)
    {
        cout << arr[i] << "\n";
    }
    cout << endl;

    // while loop
    cout << "Using a for while:\n";
    while (!done)
    {
        cout << arr[counter++] << "\n";
        if (counter == MAX_NUMBER)
            done = true;
    }
    cout << endl;

    // foreach loop
    cout << "Using a foreach loop:\n";
    for (int i : arr)
    {
        cout << i << "\n";
    }

    return 0;
}