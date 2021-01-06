#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
// declare function
void execute(string key);
// begin main
int main(int argc, string argv[])
{
    if (argc == 2)
    {
        // check if the argv[1] is a number
        int i = 0;
        while (argv[1][i] != '\0')
        {
            if (isdigit(argv[1][i]))
            {
                // if it has a number in the string 
                printf("Usage: ./vigenere keyword\n");
                return 1;
            }
            i++;
        }
        // if the program does not return 1 then open execute function
        execute(argv[1]);
        return 0;
    }
    else // if argc has more than 2 or none
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
}
// end main
// begin execute fucntion
void execute(string key)
{
    int Key[100];
    int length_Key = 0;
    string plaintext = get_string("plaintext: ");
    
    // change all key[i] into number
    for (int i = 0, length = strlen(key); i < length; i++)
    {
        string upperAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        string lowerAlphabet = "abcdefghijklmnopqrstuvwxyz";
        if (islower(key[i]))
        {
            // convert to number by using its index in the lowerAlphabet array
            for (int j = 0, n = strlen(lowerAlphabet); j < n; j++)
            {
                if (key[i] == lowerAlphabet[j])
                {
                    Key[i] = j;
                    length_Key++;
                }
            }
        }
        else 
        {
            // convert to number by using its index in the upperAlphabet array
            for (int j = 0, n = strlen(upperAlphabet); j < n; j++)
            {
                if (key[i] == upperAlphabet[j])
                {
                    Key[i] = j;
                    length_Key++;
                }
            }
        }
    }
    printf("ciphertext: ");
    // to track the Key[i] value
    int j = 0;
    for (int i = 0, length = strlen(plaintext); i < length; i++)
    {
        if (islower(plaintext[i]))
        {
            int temp = (int)(plaintext[i] + Key[j]);
            if (j == length_Key - 1)
            {
                j = 0;
            }
            else
            {
                j++;
            }
            if (temp > 'z')
            {
                temp -= 26;
            }
            printf("%c", temp);
        }
        else if (isupper(plaintext[i]))
        {
            int temp = (int)(plaintext[i] + Key[j]);
            if (j == length_Key - 1)
            {
                j = 0;
            }
            else
            {
                j++;
            }
            if (temp > 'Z')
            {
                temp -= 26;
            }
            printf("%c", temp);
        }
        else // if it is not a normal character
        {
            printf("%c", plaintext[i]);
        }
    }
    puts("");
}
