/*
    Name:
    Class:
    Project:
    Last Date:
*/
#include <iostream>
using namespace std;

string displayArray(int[], int);
string displayArray(string[], int);
void swap(int, int);
void swap(string, string);

/// @brief Here is an example of pass by value and pass by reference.
///
/// @param argc the number of arguments passed into main
/// @param argv the list of arguments passed into main
/// @return integer code indicating success or not
int main(int argc, char *argv[])
{
    // initialize int array
    int arr[]{1, 2, 3, 4, 5};
    // initialize string array
    string str[]{"one", "two", "three", "four", "five"};

    cout << "Swap two integers\n\n";
    cout << displayArray(arr, 5) << endl;
    swap(arr[1], arr[2]);
    cout << displayArray(arr, 5) << endl;

    cout << "Swap two strings\n\n";
    cout << displayArray(str, 5) << endl;
    swap(str[1], str[2]);
    cout << displayArray(str, 5) << endl;

    cout << "\n\n";
    return 0;
}

string displayArray(string arr[], int size)
{
    string results = "";
    for (int i = 0; i < size; i++)
    {
        results += arr[i] + "\n";
    }
    return results;
}

string displayArray(int arr[], int size)
{
    string results = "";
    for (int i = 0; i < size; i++)
    {
        results += to_string(arr[i]) + "\n";
    }
    return results;
}

void swap(int a, int b)
{
    int temp = a;
    a = b;
    b = temp;
}

void swap(string a, string b)
{
    string temp = a;
    a = b;
    b = temp;
}