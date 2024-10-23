/*
    Name:       Lakota Dolce
    Assignment: module 1 lab, environment setup
    Course:     Programming with C++
    Date:       08/27/2024
*/

// include library for Input/Output
#include <iostream>
#include <string>

// The preprocessor directive #define that
// simply replaces the symbol with whatever you want.
// Create new-line characters called CRLF and LINEFEED
// for retro usuage, and a TAB operator.
// You will see #define in industry, a lot!
#define CRLF "\n"  //Carriage return line feed
#define LINEFEED "\n"
#define TAB "\t"

// Below is the entry point for this application called "main".
// Main is a special function that is called when the application is executed.
// We can pass data into the function from the command line using
//  argv string array. It is an array of arrays of characters.
//  We will discuss arrays and pointers in detail later.
//
// This application simply prompts the user for their name
//  and then outputs a friendly message.
//
// To compile from folder src:  g++ -std=c++17 main1.cpp -g -o ../bin/main1
//  The -std option tells what c++ standard to compile to.
//  The -g option includes debug information into the compilation
//  The -o option tells the compiler where to put the executable and what to call it.
//
// To run from folder src: ../bin/main1
int main(int argc, char **argv) // ** symbolizes an array
{
    // define all variables at the top of the function scope
    std::string name; // Scope resolution operator (:: - together)
    std::string strAge;
    int age;

    // First, let's output the first string that is in the argv array,
    //  this will always be the path to the executable from where it is being executed from.
    // Also note the :: (scope resolution operator), we could have added "using namespace std" under the includes above instead.
    std::cout << argv[0] << "\n";
    std::cout << "argc is an integer value that holds the number of arguments when the application is executed: " << argc << CRLF;

    // capture user input from the keyboard up to the first space
    std::cout << "++++++++++++++++++++++++++++++++++++++++" << std::endl;
    std::cout << "Please enter your first name: ";
    // BEST PRACTICE: Always gather information from the user as a string, then if required, convert to a number
    std::cin >> name;

    std::cout << "Please enter your age: ";
    std::cin >> strAge;
    // Convert the string age to an integer age
    age = std::stoi(strAge);

    // output a string with the users name concatenated in the middle
    std::cout << "Hello, " << age << " years aged " << name << ", and welcome to C++!" << LINEFEED;
    std::cout << "Thanks for playing!\n";
    std::cout << "++++++++++++++++++++++++++++++++++++++++\n\n";

    // usually we return 0 for success, but we will return 200 to test the console return value.
    //  "echo $?" in powershell to echo the returned value
    //  "echo $" in terminal to echo the returned value
    return 200;
}