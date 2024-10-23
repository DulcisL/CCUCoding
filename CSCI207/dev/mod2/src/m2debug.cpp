/*
    YOUR FILE HEADER GOES HERE
*/
#include <iostream>
#include <string>
#include <iomanip>
#include <cmath>

using namespace std;

// In VS Code, if you type 3 forward slashes ///
// just above a function, it will create the header
// template that you can complete

int spendTime(void);
int spendMoreTime(void);
int spendEvenMoreTime(void);

/// @brief YOUR PROGRAM DESCRIPTION GOES HERE
/// @param argc
/// @param argv
/// @return
int main(int argc, char **argv)
{
    int returnCode = 200;
    // cout << &returnCode;
    double weekSalary;
    string strWeekSalary;
    double annualSalary;

    cout << "------------------------------------" << endl;
    cout << "|         Name: your_name          |" << endl;
    cout << "|        Class: CSCI 120 01        |" << endl;
    cout << "|   Assignment: debugging          |" << endl;
    cout << "|     Due Date: 01-01-2024         |" << endl;
    cout << "------------------------------------" << endl;

    // enter 546.11
    cout << "Please input home much you would like to make per week: ";
    cin >> strWeekSalary;

    // convert the string to a number
    weekSalary = stoi(strWeekSalary);
    // find amount in a year
    annualSalary = weekSalary * 52;

    // output to 2 decimal places
    cout << "The annual salary is: " << std::fixed << std::setprecision(2) << annualSalary << endl;

    return returnCode;
}