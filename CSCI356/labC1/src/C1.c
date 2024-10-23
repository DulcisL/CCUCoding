//------------------------------
// Lab C-1
// Name: Lakota Dolce
// Assignment: Lab C-1
// Email: lcdolce@coastal.edu
// Date: 9/17/2024 
//------------------------------

//Included libraries
#include <stdio.h>

//Takes 3 inputs and 2 ouputs
//Combines the inputs into a single digit then reverses the digits and repeats
void combine(int digit1,int digit2,int digit3,int *num,int *rev_num){
    //make the numbers
    *num = digit1*100 + digit2*10 + digit3;
    *rev_num = digit3*100 + digit2*10 + digit1;
}

//Take no input/outputs
//Calls the combine function after taking 3 digits from the user and then prints the
// result of the combine.
int main(){
    //Initialize the variables
    int digita;
    int digitb;
    int digitc;
    int num;
    int rev_num;

    //Get the digits
    printf("Enter a three digits seperated by a space: \n");
    scanf("%i %i %i", &digita, &digitb, &digitc);

    //Call function combine( input, input, input, &output, &output)
    printf("Combining numbers ... \n");
    combine(digita, digitb, digitc, &num, &rev_num);

    //print the digits
    printf("Here are the digits you chose\n %i \n", num);
    printf("\nHere are the digits backwards\n %i\n", rev_num);

    return 0;

}