/*
    Name:
    Class:
    Project:
    Last Date:
*/
#include <iostream>
using namespace std;

/// @brief
/// @param argc the number of arguments passed into main
/// @param argv the list of arguments passed into main
/// @return integer code indicating success or not
int main(int argc, char *argv[])
{
    char result;
    cout << "Do you want to get loopy? ";
    // is this an infinite loop?
    while (true)
    {
        cin >> result; // note that you must hit the enter key to process

        if (result == 'y' || result == 'Y')
        {
            cout << "Continuing to the next iteration of the while loop ";
            continue;
        }
        else
        {
            cout << "Breaking out of the while loop ";
            break;
        }
    }

    return 0;
}