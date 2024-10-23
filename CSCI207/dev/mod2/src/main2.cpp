#include <iostream>

using namespace std;

#define FOREGROUND_BLACK 30
#define FOREGROUND_RED 31
#define FOREGROUND_GREEN 32
#define FOREGROUND_YELLOW 33
#define FOREGROUND_BLUE 34
#define FOREGROUND_MAGENTA 35
#define FOREGROUND_CYAN 36
#define FOREGROUND_WHITE 37

#define BACKGROUND_BLACK 40
#define BACKGROUND_GREEN 41
#define BACKGROUND_RED 42
#define BACKGROUND_YELLOW 43
#define BACKGROUND_BLUE 44
#define BACKGROUND_MAGENTA 45
#define BACKGROUND_CYAN 46
#define BACKGROUND_WHITE 47

#define TOP_LEFT_CORNER "\u250F"
#define TOP_RIGHT_CORNER "\u2513"
#define BOTTOM_LEFT_CORNER "\u2517"
#define BOTTOM_RIGHT_CORNER "\u251B"

#define HORIZONTAL_ELEMENT "\u2501"
#define VERTICAL_ELEMENT "\u2503"

string ChangeTextColor(int text_color)
{
    return "\033[1;" + to_string(text_color) + "m";
}

string ChangeBackgroundColor(int background_color)
{
    return "\033[1;" + to_string(background_color) + "m";
}

int main(int argc, char **argv)
{
    // To see all box-form symbols, uncomment below
    cout << "\n\n\tHere are some of the box shapes available:\n\t" << "\u2501" << " " << "\u2503" << " " << "\u250F" << " " << "\u2513" << " " << "\u2517" << " " << "\u251B" << " " << "\u2523" << " " << "\u252B" << " " << "\u2533" << " " << "\u253B" << " " << "\u254B" << "\n\n";

    const int array_size = 5;
    // Create a string array using an initializer list

    cout << ChangeTextColor(FOREGROUND_MAGENTA);
    cout << "\n\tHere is some text to test text color!\n";

    cout << ChangeTextColor(FOREGROUND_GREEN);
    cout << "\n\tThanks for playing, bye bye!\n\n\n";
}

/*

You need to output ANSI colour codes. Note that not all terminals support this; if colour sequences are not supported, garbage will show up.
Example:
 cout << "\033[1;31mbold red text\033[0m\n";

Here, \033 is the ESC character, ASCII 27. It is followed by [, then zero or more numbers separated by ;, and finally the letter m. The numbers describe the colour and format to switch to from that point onwards.
The codes for foreground and background colours are:

     foreground background
black        30         40
red          31         41
green        32         42
yellow       33         43
blue         34         44
magenta      35         45
cyan         36         46
white        37         47

reference: https://stackoverflow.com/questions/2616906/how-do-i-output-coloured-text-to-a-linux-terminal

*/