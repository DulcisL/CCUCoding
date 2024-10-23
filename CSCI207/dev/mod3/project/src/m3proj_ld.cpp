/*
    Name: Lakota Dolce
    Class: CSCI207
    Project: Project 3
    Last Date: 9/8/2024
*/
#include <iostream>
#include <ctime>
using namespace std;

/// @brief 
/// @param none
/// @return string of menu
int Menu(){
    cout << "Welcome to the War Games \n";
    cout << "Please choose from the following: \n";
    cout << "1) Random Number Game \n2) Lottery \n3) Exit \n";
    return 0;
}

/// @brief
/// @param none
/// @return nothing
int RandomNumber(){
    // see modulo operator
    
    int number = rand() %101;
    int choice;
    int guess = 0;

    //Create loop to check user choice and rerun
    while (choice != number){
        cout << "Please choose a number between 0 and 100: \n";

        //Get user choice
        cin >> choice;

        //Error check
        if (cin.fail()){

            //Clear cin so you don't get stuck in infinite loop
            cin.clear();
            cin. ignore(10000, '\n');
            cout << "\n*That was not a valid choice* \n\n";
            continue;
        }
        if (choice < 0 || choice > 100){
            cout << "Your guess is not between 0 and 100 \n";
            continue;
        }

        //Check if hi/lo and tell user
        if (choice < number) {
            cout << "Your guess was low \n";
            guess +=1;
            continue;
        }
        if (choice > number) {
            cout << "Your guess was high \n";
            guess +=1;};
            continue;
    }
    cout << "\nCongratulations you guessed the number in ", guess, " guesses \n";
    
    return 0;
    
}

/// @brief
/// @param none
/// @return none
int Lottery(){
    // Create loop to get the numbers
    cout << "The lucky numbers are: \n";

    for (int i = 0; i < 5; i++) {
        //Initialize
        int upper = 50;
        int lower = 0;
        //Get random numbers
        if (i == 4){
            cout << "Drumroll please \n. \n. \n. \n";
        }
        cout << (rand() % (upper - lower + 1)) + lower << " \n";
        
    }

    return 0;
}

/// @brief
/// @param argc the number of arguments passed into main
/// @param argv the list of arguments passed into main
/// @return integer code indicating success or not
int main(int argc, char* argv[]){

    //Create loop for game
    while (true){

        //Initialize 
        int choice;
        // seed the random number machine
        srand(time(nullptr));

        //Print menu
        Menu();

        //take user choice
        cin >> choice;

        //Error check
        if (cin.fail()){

            //Clear cin so you don't get stuck in infinite loop
            cin.clear();
            cin. ignore(10000, '\n');
            cout << "\n*That was not a valid choice* \n\n";
            continue;
        }
        if (choice < 1 || choice > 3){
            cout << "\n*That was not a valid choice* \n\n";
            continue;
        }

        //Break sequence
        if (choice == 3){
            break;
        }
        
        //Check choice for game and run
        if (choice ==1){
            RandomNumber();
            continue;
        }
        if (choice ==2){
            Lottery();
            continue;
        }
    }

    cout << "\nGoodbye";
}