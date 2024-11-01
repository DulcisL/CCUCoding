/*
    Name: Lakota Dolce
    Class: CSCI207-01
    Project: Module 5
    Last Date: 09/22/2024
*/
#include <iostream>
#include <fstream>
#include <iomanip>
#include <string> // for string length checks

using namespace std;

#define FILE_NAME "../data/reviews.txt"
#define MAX_REVIEWS 10

// user defined data type
struct GameInfo
{
    string GameName;
    string Review;
    float Rating;

    string toString()
    {
        return GameName + "\t" + Review + "\t" + to_string(Rating) + "\n";
    }
};

// function prototypes
unsigned long long getFileSize();
string displayAllReviews();
void writeReviewsToFile();
void readReviewsFromFile();
void enterNewReview();

// global variables
GameInfo Reviews[MAX_REVIEWS];
int reviewsCounter = 0;

///
/// @brief This application will use functions, arrays, files, and we will also use cmake to compile and link
///         When the application opens, it reads in the contents of the reviews.txt file; it does not display the contents.
///         The user will be shown a menu that allows:
///             1. Show reviews from file
///             2. Add a new review
///             3. Save reviews to file
///             4. Exit
///         The menu should be in a loop until the user types 4.
///         If user types 1, show all reviews that was read in at opening
///             Use a function to show all the reviews
///         If user types 2, add a new review to the array of reviews. Do not write to file yet
///             Use a function to capture a new review and add to array
///         If user types 3, write all reviews to the file overwriting what was there initially
///             Use a function to write array to file
///
///         Assume user will enter valid data.
///
/// @param argc the number of arguments passed into main
/// @param argv the list of arguments passed into main
/// @return integer code indicating success or not
int main(int argc, char *argv[])
{

    string input;
    // GameInfo Reviews[MAX_REVIEWS];
    int fileSize = getFileSize();

    if (fileSize == 0)
    {
        cout << "No reviews yet, would you like to create one now? ";
        getline(cin, input);
        if (input == "Y" || input == "y")
        {
            enterNewReview();
        }
    }

    //Initialize
    int choice;
    input = "";
    // Get file reviews
    try{
        //Read in reviews from the file
        readReviewsFromFile();
    }
    //Catch exceptions **fix with actual exceptions
    catch(exception){
        cout << "I couldn't read from the file \n";
    }

    while (choice != 4){
        //Print menu
        cout << "---------------------------------\n";
        cout << "Please choose from the following\n";
        cout << "1. Show reviews from file\n";
        cout << "2. Add a new review\n";
        cout << "3. Save reviews to file\n";
        cout << "4. Exit\n";
        cout << "---------------------------------\n";

        //Get choice and error check
        cin >> input;
        try{
            //check length
            if (input.length() > 1){
                throw std::out_of_range("Too many characters were input.\n");
            }

            choice = std::stoi(input);
            //If the cin fails
            if (cin.fail()){
                //Clear cin so you don't get stuck in infinite loop
                cin.clear();
                cin.ignore(10000, '\n');
                throw invalid_argument("Argument was not a number");        
                }
            //if the choice is out of range
            if (choice > 4 || choice < 1){
                throw std::out_of_range("Choice was not within range of available");
            }

            //Check user choice
            if (choice == 4){
                //return to break loop
                continue;
            }
            if (choice == 1){
            // Test reading from file then displaying contents
            // readReviewsFromFile();
            // cout << displayAllReviews();
                
                cout << "---------------------------------\n";
                cout << displayAllReviews() << "\n";
                cout << "---------------------------------\n";
            }
            if (choice == 2){
            // Add new test review
                enterNewReview();
                //Show reviews
                displayAllReviews();
            }
            if (choice == 3){
            // test write to file from array
                writeReviewsToFile();
            }
        }
        //Catch out of range errors
        catch (out_of_range){
            cout << "Choice was out of range, please try again\n";
            //Clear cin so you don't get stuck in infinite loop
            cin.clear();
            cin. ignore(10000, '\n');
            continue;
        }
        //Catch any bad inputs when trying to convert
        catch (invalid_argument){
            //Clear cin so you don't get stuck in infinite loop
            cin.clear();
            cin. ignore(10000, '\n');
            cout << "That was not a valid choice, please try again \n";
            continue;
        }
    }
    return 0;
}

string displayAllReviews()
{
    try{
        //Read in reviews in array
        string temp = "";
        for (int i = 0; i < reviewsCounter; i++)
        {
            if (Reviews[i].toString() != "\t")
            {
                temp += Reviews[i].toString();
            }
        }
        return temp;
    }
    catch(exception){
        cout << "I failed getting the info from the file\n";
    }
    return "";
}

void enterNewReview()
{
    //Initialize
    string input;

    while (true){
        //Error checking
        //reviewCounter !> 10 causes segmentation fault
        //Start overwriting
        if (reviewsCounter >= 10){
            reviewsCounter = 0;
        }
        try{
            while(true){
                try{
                    //Clear any previous inputs
                    cin.clear();
                    cin.ignore(10000, '\n');
                    //get the user game name
                    cout << "Enter name of game must be less than 60 characters: ";
                    getline(cin, input);

                    //Check if the name is less than 60 characters
                    if (input.length() > 60){
                        throw std::out_of_range("The input was too long\n");
                    }
                    else {
                        Reviews[reviewsCounter].GameName = input;
                        break;
                    }
                }
                catch (out_of_range){
                    cout << "The input was too large please try again.\n";
                    continue;
                }
            }
            while (true){
                try{
                    //Take user input or the review desc
                    cout << "Enter review less than 256 characters long: ";
                    getline(cin, input);

                    //Error check
                    if (input.length() > 256){
                        throw std::out_of_range("The input was too long\n");
                    }
                    else {Reviews[reviewsCounter].Review = input;break;}
                }
                catch (out_of_range){
                    cout << "The input was too large please try again.\n";
                    continue;
                }
            }
            while (true){
                try{
                    //Get user input for the rating
                    cout << "Enter rating out of 10: ";
                    getline(cin, input);

                    //Error check
                    if (input.length() > 4){
                        throw std::out_of_range("The input was too long\n");
                    }
                    if (stof(input) <= 10 && stof(input) > 0){
                        Reviews[reviewsCounter].Rating = stof(input);
                        
                        //print review
                        cout << Reviews[reviewsCounter].toString() << "\n";
                        //implement the review counter if less than 10 see above
                        //otherwise start writing over
                        if (reviewsCounter < 10){
                            reviewsCounter ++;
                        }
                        else {reviewsCounter = 0;}
                        
                        return;
                    }
                    else {
                        throw std::out_of_range("Rating was not out of 10");
                    }
                }
                catch (out_of_range){
                    cout << "The input was not within 0 and 10, please try again.\n";
                    continue;
                }
                catch (invalid_argument)
                {
                    cout << "Not a valid input, please try again \n";
                    continue;
                }
            }
        }
        //Catch anything else and log
        catch(exception) {
            cout << "Something unaccounted for happened, please try again.\n";
            cout << input << " was the last input.\n";
        }
        break;
    }
    return;
}

void readReviewsFromFile()
{

    // Open the input file
    ifstream inputFile(FILE_NAME);
    // GameInfo games[MAX_REVIEWS];

    // Check if the file is successfully opened
    if (!inputFile.is_open())
    {
        cerr << "Error opening the file!" << endl;
    }
    else
    {
        string line;
        int i = 0;
        while (getline(inputFile, line))
        { 
            // find first tab
            int end = line.find("\t");
            // game name
            //Prevent picking up empty slots
            if (line == "\t"){
                break;
            }
            // cout << line.substr(0, end) << endl;
            Reviews[i].GameName = line.substr(0, end);

            // remove delimiter
            line.erase(line.begin(), line.begin() + end + 1);
            // find next delimiter
            end = line.find("\t");

            // Review
            // cout << line.substr(0, end) << endl;
            Reviews[i].Review = line.substr(0, end);

            // remove delimiter
            line.erase(line.begin(), line.begin() + end + 1);
            // find next delimiter
            end = line.find("\t");

            // Rating
            // cout << line.substr(0, end) << endl;
            //round to a single decimal
            Reviews[i].Rating = stof(line.substr(0, end));

            i++;
            //Causes segmentation fault when reviewCounter >= MAX_REVIEWS
            //Make program overwrite after that
            if (reviewsCounter < 10){
                reviewsCounter ++;
            }
        }
    }

    // Close the file
    inputFile.close();

    return;
}

void writeReviewsToFile()
{
    ofstream myfile(FILE_NAME);
    if (myfile.is_open())
    {
        for (int i = 0; i < reviewsCounter; i++)
        {
            //Prevent writing of empty reviews
            if (Reviews[i].toString() == "\t"){
                break;
            }
            myfile << Reviews[i].toString();
        }
    }
    else
    {
        // default error stream, could be a log file for example
        cerr << "Error opening file: " << FILE_NAME << std::endl;
    }
    myfile.close();
}

/// @brief
/// @return
unsigned long long getFileSize()
{
    std::streampos fsize = 0;
    std::ifstream myfile(FILE_NAME, ios::in);

    // check file open for errors
    if (!myfile.is_open())
    {
        // default error stream, could be a log file for example
        cerr << "Error opening file: " << FILE_NAME << std::endl;
    }

    fsize = myfile.tellg();         // The file pointer is currently at the beginning
    myfile.seekg(0, ios::end);      // Place the file pointer at the end of file
    fsize = myfile.tellg() - fsize; // Take the difference

    // release resource!
    myfile.close();

    return fsize;
}