/* Create a function that makes every other letter (character) uppercase starting at 0
hello => HeLlO
HELLO => HeLlO
*/

const stringFormat = (string) => {
    var newString = ""
    for (let i = 0;  i <string.length -1; i_++){
        if (i % 2 == 0 || i == 0){
            newString += string[i].toUpperCase;
        }
        if (i % 2 != 0 && i != 0){
            newString += string[i].toLowerCase;
        }
    }
    return newString;
}

console.log(stringFormat("Hello"));
