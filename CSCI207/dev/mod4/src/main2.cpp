/*
    Name:
    Class:
    Project:
    Last Date:
*/
#include <iostream> // cin cout
#include <fstream>  // file input
#include <iomanip>  // manipulate output

using namespace std;

// File layout:
// FirstName LastName Pos AVG OBP SLG HITS HR RBI RUNS SB
//Public class-like
struct PlayerStruct
{
    // Modify this structure
    string FirstName;
    string LastName;
    string Position;
    float Average;
    float OnBasePerctage;
    float SluggingPercentage;
    int TotalHits;
    int TotalHomeRuns;
    int TotalRunsBattedIn;
    int Runs;
    int StolenBases;
};

/// @brief Trim the whitespace from a both ends of a string
/// @param str is the string that needs to be trimmed
/// @return a string that has been trimmed
string TrimString(string str)
{
    const string whiteSpaces = " \t\n\r\f\v";
    // Remove leading whitespace
    size_t first_non_space = str.find_first_not_of(whiteSpaces);
    str.erase(0, first_non_space);
    // Remove trailing whitespace
    size_t last_non_space = str.find_last_not_of(whiteSpaces);
    str.erase(last_non_space + 1);
    return str;
}

/// @brief Read all players in from file HOFPlayers.txt file.
///         Process all records and at minimum display a menu that allows the user to:
///             1 Print all HOF Players: Full Name, Position, Batting Average and give all players BA at the bottom
///             2 Print all stats for players for a single position entered by user
//              3 Exit
///         The menu should be in a loop that allows the user to select different options until exit is selected.
/// @param argc the number of arguments passed into main
/// @param argv the list of arguments passed into main
/// @return integer code indicating success or not
int main(int argc, char *argv[])
{
    // process all input as a string then parse to float or int as needed
    string input;

    // object to read in file from file stream
    ifstream inputFile;

    // Use a counter to parse text file
    int counter = 0;

    // Create an array with 9 players in it (Team)
    const int ArraySize = 175;
    PlayerStruct Players[ArraySize];

    // Open an output file.
    inputFile.open("../data/HOFPlayers.txt");

    // Remember that all arrays start with a 0 index
    while (counter < 175)
    {
        inputFile >> input;
        Players[counter].FirstName = TrimString(input);

        inputFile >> input;
        Players[counter].LastName = TrimString(input);

        inputFile >> input;
        Players[counter].Position = TrimString(input);

        inputFile >> input;
        //Players[counter].Average = std::stof(TrimString(input));

        // need to process input
        inputFile >> input;
        inputFile >> input;

        inputFile >> input;
        Players[counter].TotalHits = stoi(TrimString(input));

        // need to process input
        inputFile >> input;
        inputFile >> input;
        inputFile >> input;
        inputFile >> input;

        // increment loop counter
        counter++;
    }

    // Print Output Header
    cout << setw(20) << "Full Name" << setw(5) << "Pos" << setw(10) << "Avg" << setw(10) << "Hits";
    cout << endl;
    cout << setw(20) << "---------" << setw(5) << "---" << setw(10) << "---" << setw(10) << "----";
    cout << endl;

    // Use a foreach loop to output the array of Players
    for (PlayerStruct player : Players)
    {
        cout << setw(20) << player.FirstName + " " + player.LastName << setw(5) << player.Position << setw(10) << fixed << showpoint << setprecision(3) << player.Average << setw(10) << player.TotalHits << "\n";
    }

    return 0;
}