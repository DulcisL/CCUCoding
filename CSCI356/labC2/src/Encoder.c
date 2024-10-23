/*
Lakota Dolce
CSCI356
Lab C2
Dr. Fuchs
*/

//Included libraries
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to save data to a file
void FileSave (char* input, const char* fileLocation) {
    //Open the file
    FILE *file = fopen(fileLocation, "w");
    //Check if file exists
    if (file != NULL) {
        //read from file and close it
        fprintf(file, "%s ", input);
        fclose(file);
    } else {
        //If file doesn't exist let user know there was an error
        printf("Error opening file.\n");
    }
}
// Function to read data from a file
void FileRead (char* output, const char* fileLocation) {
    //open the file
    FILE *file = fopen(fileLocation, "r");
    //Check if file exists
    if (file != NULL) {
        //Read in up to 100 characters
        fgets(output, 100, file);
        //close the file
        fclose(file);
    } else {
        //Otherwise tell user there was an error
        printf("Error opening file.\n");
    }
}

// Function to Encode text  from the input and output the encoded message
void  EncodeTxt (char* input, char* output){
    // Initialize loop variables
    int length = strlen(input);
    // Make an array to store the encoded characters
    char message[3 * length + 1];
    int index = 0;
    //make loop to check the characters of the message
    for (int i = 0; i < length; i++) {
        //Implement switch case to compare the characters and encode them to the output
        switch (input[i]) {
            case 'a': case 'A': strcpy(&output[index], "10 "); break;
            case 'b': case 'B': strcpy(&output[index], "11 "); break;
            case 'c': case 'C': strcpy(&output[index], "12 "); break;
            case 'd': case 'D': strcpy(&output[index], "13 "); break;
            case 'e': case 'E': strcpy(&output[index], "14 "); break;
            case 'f': case 'F': strcpy(&output[index], "15 "); break;
            case 'g': case 'G': strcpy(&output[index], "16 "); break;
            case 'h': case 'H': strcpy(&output[index], "17 "); break;
            case 'i': case 'I': strcpy(&output[index], "18 "); break;
            case 'j': case 'J': strcpy(&output[index], "19 "); break;
            case 'k': case 'K': strcpy(&output[index], "20 "); break;
            case 'l': case 'L': strcpy(&output[index], "21 "); break;
            case 'm': case 'M': strcpy(&output[index], "22 "); break;
            case 'n': case 'N': strcpy(&output[index], "23 "); break;
            case 'o': case 'O': strcpy(&output[index], "24 "); break;
            case 'p': case 'P': strcpy(&output[index], "25 "); break;
            case 'q': case 'Q': strcpy(&output[index], "26 "); break;
            case 'r': case 'R': strcpy(&output[index], "27 "); break;
            case 's': case 'S': strcpy(&output[index], "28 "); break;
            case 't': case 'T': strcpy(&output[index], "29 "); break;
            case 'u': case 'U': strcpy(&output[index], "30 "); break;
            case 'v': case 'V': strcpy(&output[index], "31 "); break;
            case 'w': case 'W': strcpy(&output[index], "32 "); break;
            case 'x': case 'X': strcpy(&output[index], "33 "); break;
            case 'y': case 'Y': strcpy(&output[index], "34 "); break;
            case 'z': case 'Z': strcpy(&output[index], "35 "); break;
            default: strcpy(&output[index], "   "); break;
        }
        //Increase index by 3 for code length
        index += 3; // move index for next 3-char sequence
    }
    //check the null pointer
    output[index] = '\0';
}

// Function to Decode text from input and return in output
void DecodeTxt (char* input, char* output){
    //Initialize loop variables
    int length = strlen(input);
    //decode into single letters
    char message[length / 3 + 1];
    int index = 0;

    //Make loop
    for (int i = 0; i < length; i += 3) {
        //set up the code to read
        char code[3];
        strncpy(code, &input[i], 2);
        //check the null pointer
        code[2] = '\0';
        //Implement switch case to compare the numbers and decode them
        //conver code to an int
        switch (atoi(code)) {
            case 10: output[index] = 'A'; break;
            case 11: output[index] = 'B'; break;
            case 12: output[index] = 'C'; break;
            case 13: output[index] = 'D'; break;
            case 14: output[index] = 'E'; break;
            case 15: output[index] = 'F'; break;
            case 16: output[index] = 'G'; break;
            case 17: output[index] = 'H'; break;
            case 18: output[index] = 'I'; break;
            case 19: output[index] = 'J'; break;
            case 20: output[index] = 'K'; break;
            case 21: output[index] = 'L'; break;
            case 22: output[index] = 'M'; break;
            case 23: output[index] = 'N'; break;
            case 24: output[index] = 'O'; break;
            case 25: output[index] = 'P'; break;
            case 26: output[index] = 'Q'; break;
            case 27: output[index] = 'R'; break;
            case 28: output[index] = 'S'; break;
            case 29: output[index] = 'T'; break;
            case 30: output[index] = 'U'; break;
            case 31: output[index] = 'V'; break;
            case 32: output[index] = 'W'; break;
            case 33: output[index] = 'X'; break;
            case 34: output[index] = 'Y'; break;
            case 35: output[index] = 'Z'; break;
            default: output[index] = ' ';
        }
        //increase index by 1
        index++;
    //check null pointer
    output[index] = '\0';
    }
}

// Main function
int main(){
    //Initialize the variables needed
    char choice;
    char message[100];
    char output[100];
    char location[100];

    //Create a loop to run the menu
    while (choice != '5') {
        printf("---------------------------------------------\n");
        printf("Welcome to the Encoder Program \n");
        printf("Please choose from the following:\n");
        printf("1) Encode a phrase in the unencoded file\n");
        printf("2) Decode a message from the decode file\n");
        printf("3) Encode a message from the console input\n");
        printf("4) Decode a message from the console input \n");
        printf("5) Exit the program\n");
        printf("---------------------------------------------\n");
        scanf(" %c", &choice);

        // Check for end condition
        if (choice == '5') {
            break;
        }

        // Error check
        if (choice < '1' || choice > '5') {
            //Tell user there was an error and restart the loop
            printf("That was not a valid input, please try again.\n");
            continue;
        }

        // Logic check
        if (choice == '1') {
            // Get message from the unencoded file (../unencoded.txt)
            FileRead(message, "./unencoded.txt");
            // Call function to encode
            EncodeTxt(message, output);
            //Print the message
            printf("The message was %s\n", output);
            //save output to encoded.txt
            FileSave(output, "./encoded.txt");
        }

        if (choice == '2') {
            // Get message from the encoded file (../encoded.txt)
            FileRead(message, "./encoded.txt");
            // Call function to decode
            DecodeTxt(message, output);
            //Print the message
            printf("The message was %s\n", output);
            //save output to encoded.txt
            FileSave(output, "./unencoded.txt");
        }
        if (choice == '3') {
            // Get user input for encoding
            printf("Enter the message to encode: \n");
            scanf(" %[^\n]%*c", message);
            // Call the encode input function
            EncodeTxt(message, output);
            //print to the console
            printf("The message was %s \n", output);
            
            // Ask user if they would like to save the file
            printf("Do you want to save the file? (Y or N) \n");
            //Get user choice
            scanf(" %c", &choice);
            if (choice == 'Y' || choice == 'y'){
                //Ask user the location they would like to save the file
                printf("Where do you want to save the file? \n");
                scanf(" %s", location);
                FileSave(output, location);
            }
            //If user doesn't want to save then restart the loop
            if (choice =='N' || choice == 'n'){
                continue;
            }
        }

        if (choice == '4') {
            // Get user input for decoding
            printf("Enter the encoded message: \n");
            scanf(" %[^\n]%*c", message);
            // Call the decode input function
            DecodeTxt(message, output);
            //print to the console
            printf("The message was %s\n", output);

            // Ask user if they would like to save the file
            printf("Do you want to save the file? (Y or N) \n");
            //Get user choice
            scanf(" %c", &choice);
            if (choice == 'Y' || choice == 'y'){
                //Ask user the location they would like to save the file
                printf("Where do you want to save the file? \n");
                scanf(" %s", location);
                //Save the file to the appropriate name and location.
                FileSave(output, location);
            }
            //If user doesn't want to save then restart the loop
            if (choice =='N' || choice == 'n'){
                continue;
            }
        }
    }
    return 0;
}