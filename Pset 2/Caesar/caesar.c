#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
// declare function 
void execute(string key);
int changeKeyToNum(string key);
void stringToNum(string plaintext);
void numtoString(int int_ciphertext[], int isLower, int length);
// begins main function
int main(int argc, string argv[])
{
    // check the user is following the struction
    if (argc == 2)
    {
        bool check = false;
        for (int i = 0, length = strlen(argv[1]); i < length; i++)
        {
            if (argv[1][i] >= 'A' && argv[1][i] <= 'z')
            {
                check = true;
            } 
        }
        // if the command-line arg is a string, print out caution.
        if (check)
        {
            puts("Usage: ./caasar key");
            return 1;
        }
        else 
        {
            // begin to execute the program
            execute(argv[1]);
            return 0;
        }
    } 
    else 
    {
        puts("Usage: ./caasar key");
        return 1;
    }
}
// end main function
void execute(string key)
{
    string plaintext = get_string("plaintext: ");
    // declare variables
    int Key = atoi(key) % 26;
    
    printf("ciphertext: ");
    for (int i = 0, length = strlen(plaintext); i < length; i++)
    {
        // check if lower case
        if (islower(plaintext[i]))
        {
            int temp = (int)(plaintext[i] + Key);
            // if it exceeds number 'z' minus it 26
            if (temp > 'z')
            {
                temp -= 26;
            }
            printf("%c", temp);
        } 
        else if (isupper(plaintext[i]))
        {
            int temp = (int)(plaintext[i] + Key);
            // if it exceeds number 'Z' minus it 26
            if (temp > 'Z')
            {
                temp -= 26;
            }
            printf("%c", temp);
        }
        else // if it is a special character 
        {
            printf("%c", plaintext[i]);
        }
    }
    puts("");
}
