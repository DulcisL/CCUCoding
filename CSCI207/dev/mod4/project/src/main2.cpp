/*
    Name: Lakota Dolce 
    Class: CSCI207-01
    Project: Module 4 Project
    Last Date: 09/15/2024
*/
#include <iostream> // cin cout
#include <fstream>  // file input
#include <iomanip>  // manipulate output

using namespace std;

// File layout:
// FirstName LastName Pos AVG OBP SLG HITS HR RBI RUNS SB
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

/// @brief Option 1: Print all HOF Players: Full Name, Position, Batting Average and give all players BA at the bottom
/// @param argc the number of arguments passed into Option1 = 1
/// @param argv the list of arguments passed into main: {Players}
/// @return integer code indicating success or not: 0

int Option1 (PlayerStruct Players[], int size){
    // Print Output Header
    cout << setw(20) << "Full Name" << setw(5) << "Pos" << setw(10) << "Avg" << setw(10) << "Hits";
    cout << endl;
    cout << setw(20) << "---------" << setw(5) << "---" << setw(10) << "---" << setw(10) << "----";
    cout << endl;

    float total = 0;
    // Use a foreach loop to output the array of Players and get averages
    for (int i = 0; i < size; i++){
        cout << setw(20) << Players[i].FirstName + " " + Players[i].LastName << setw(5) << Players[i].Position << setw(10) << fixed << showpoint << setprecision(3) << Players[i].Average << setw(10) << Players[i].TotalHits << "\n";
        //Run through each player and read in each average
        total += Players[i].Average;
    }
    //Calculate average
    float totalAvg = total / size;
    //Display total batting average
    cout << setw(20) << "\nTotal Batting Avg: " << setw(5) << fixed << showpoint << setprecision(3) << totalAvg;
    cout << endl;

    return 0;
}


/// @brief Option 2: Print all stats for players for a single position entered by user
/// @param argc the number of arguments passed into main
/// @param argv the list of arguments passed into main
/// @return integer code indicating success or not

int Option2(PlayerStruct Players[], int size){
    //Initialize
    string choice = "";
    int badInput = 1;
    PlayerStruct Positions [28];
    int counter = 0;
    int pos = 0;
    string positions [8] = {"1B", "2B", "3B", "SS", "C", "LF", "CF", "RF"};

    //Take in user choice for pos
    while (badInput == 1){
        cout << "What Position would you like to see the stats for? \n";
        cin >> choice;

        //Convert to capitals
        try{
            for (char& c: choice){
            c = std::toupper(c);
            }
            for (int i = 0; i <= sizeof(positions); i++){
                if (i < sizeof(positions) && choice == positions[i]){
                    badInput = 0;
                    break;
                }
                if (i == sizeof(positions)){
                    cout << "Not a valid choice\n";
                    throw std::invalid_argument("Not a choice");
                }
            }
        //Error Check
        }
        catch (exception){
            cout << "That was not a valid choice";
        }
    }
    

    //Create loop to search for positon
    while (counter < size)
    {
        //Read in only the players of a pos
        if (Players[counter].Position == choice){
            //Add them to the new array
            Positions[pos] = Players[counter];
            pos ++;
        }
        // increment loop counter
        counter++;
    }
    
    
    //print out the information
    // Print Output Header
    cout << setw(20) << "Full Name" << setw(5) << "Pos" << setw(10) << "Avg" << setw(10) << "Hits";
    cout << endl;
    cout << setw(20) << "---------" << setw(5) << "---" << setw(10) << "---" << setw(10) << "----";
    cout << endl;

    //Create loop to print player info
    for (PlayerStruct player : Positions)
    {
        //Print out the information
        if (player.FirstName != ""){
            cout << setw(20) << player.FirstName + " " + player.LastName << setw(5) << player.Position << setw(10) << fixed << showpoint << setprecision(3) << player.Average << setw(10) << player.TotalHits << "\n";

        }
        else break;
    }
    
    return 0;
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
    //Must be in the directory or data won't read in
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
        Players[counter].Average = std::stof(TrimString(input));

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
    //Create Menu
    //Initialize variables
    int choice = 0;
    input = "";
    //Create loop
    while (choice !=3){
        cout << "\n_______________________________________\n";
        cout << "*     Welcome to the HOF Data Reader    *\n";
        cout << "* Please Choose from the following menu *\n";
        cout << "*1) List all HOF Members, Pos, Avg, Hits*\n";
        cout << "* 2)All Stats for players in a position *\n";
        cout << "*              3) Exit                  *\n";
        cout << "\n_______________________________________\n";

        //error check
        cin >> input;
        try{
            choice = stoi(TrimString(input));
            if (choice < 1 || choice >3){
                // throw error
                throw std::invalid_argument("Number out of range");
            }
            if (choice == 1){
                //Call function 1
                Option1(Players, ArraySize);
                continue;
            }
            if (choice == 2) {
                //Call function 2
                Option2(Players, ArraySize);
                continue;
            }
            if (choice == 3){
                //Exit the program
                cout << "Goodbye\n";
                break;
            }
        }
        catch (const std::invalid_argument){
            cout << "\nThat was not a valid input, please try again \n";
            continue;
        }    
        continue;
    }

    return 0;
}