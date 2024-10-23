/*
    Name: Lakota Dolce
    Class: CSCI207
    Project: mod2
    Last Date: 9/3/2024
*/
#include <iostream>
#include <string>

#define BACKGROUND_GREEN 42
#define BACKGROUND_RED 41
#define BACKGROUND_BLUE 44

#define FOREGROUND_GREEN 32
#define FOREGROUND_RED 31
#define FOREGROUND_BLUE 34

using namespace std;

//Function purpose -> Change the text color
//Input -> Nothing
//Output -> ANSI code in string format

string ChangeTextColor(){

    //Initialize variables
    int textColor = 0;

    //Print Menu
    cout << "What color do you want the text?\n";
    cout << "1) Red \n2) Green \n3) Blue \n";
    cin >> textColor;

    //Check input / Error check
    if (textColor == 1){
        textColor = FOREGROUND_RED;
        return "\033[1;" + to_string(textColor) + "m";
    }
    if (textColor == 2){
        textColor = FOREGROUND_GREEN;
        return "\033[1;" + to_string(textColor) + "m";
    }
    if (textColor == 3){
        textColor = FOREGROUND_BLUE;
        return "\033[1;" + to_string(textColor) + "m";
    }
    else {
        cout << "You didn't choose from the menu, please try again...\n";
        return ChangeTextColor ();
        }
}

//Function purpose -> Change the background color
//Input -> Nothing
//Output -> ANSI code in string format


string ChangeBackgroundColor(){

    //Initialize variables
    int backgroundColor = 0;

    //Print Menu
    cout << "What color do you want the background?\n";
    cout << "1) Red \n2) Green \n3) Blue \n";
    cin >> backgroundColor;

    //Check input / Error check
    if (backgroundColor == 1){
        backgroundColor = BACKGROUND_BLUE;
        return "\033[1;" + to_string(backgroundColor) + "m";
    }
    if (backgroundColor == 2){
        backgroundColor = BACKGROUND_GREEN;
        return "\033[1;" + to_string(backgroundColor) + "m";
    }
    if (backgroundColor == 3){
        backgroundColor = BACKGROUND_BLUE;
        return "\033[1;" + to_string(backgroundColor) + "m";
    }
    else {
        cout << "You didn't choose from the menu, please try again...\n";
        return ChangeBackgroundColor();
    }
    
}


/// @brief
/// @param argc the number of arguments passed into main
/// @param argv the list of arguments passed into main
/// @return integer code indicating success or not
int main(int argc, char* argv[])
{
    //Call the functions to edit the output
    cout << ChangeTextColor();
    cout << ChangeBackgroundColor();
    
    //Print the app header after changes
    cout << "\n\t *********************"<< endl;
    cout << "\n\t| Name: Lakota Dolce  |" << endl;
    cout << "\n\t| Class: CSCI207      |" << endl;
    cout << "\n\t| Project: mod 2      |" << endl;
    cout << "\n\t| Last Date: 9/3/2024 |" << endl;
    cout << "\n\t *********************"<< endl;
}