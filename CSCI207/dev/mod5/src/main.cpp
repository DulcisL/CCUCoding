/*
    Name:
    Class:
    Project:
    Last Date:
*/
#include <iostream>
#include <fstream>

using namespace std;

#define FILE_NAME "../data/reviews.txt"
#define MAX_REVIEWS 10

// user defined data type
struct GameInfo
{
    string GameName;
    string Review;
    int Rating;

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

    // Test reading from file then displaying contents
    // readReviewsFromFile();
    // cout << displayAllReviews();

    // Add new test review
    // enterNewReview();

    // test wrtie to file from array
    // writeReviewsToFile();

    return 0;
}

string displayAllReviews()
{
    string temp = "";
    for (int i = 0; i < reviewsCounter; i++)
    {
        temp += Reviews[i].toString();
    }
    return temp;
}

void enterNewReview()
{
    string input;
    cout << "Enter name of game: ";
    getline(cin, input);
    Reviews[reviewsCounter].GameName = input;

    cout << "Enter review: ";
    getline(cin, input);
    Reviews[reviewsCounter].Review = input;

    cout << "Enter rating: ";
    getline(cin, input);
    Reviews[reviewsCounter].Rating = stoi(input);

    // increase array index
    reviewsCounter++;
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
            Reviews[i].Rating = stoi(line.substr(0, end));

            i++;
            reviewsCounter++;
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