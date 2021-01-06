/*
    Ngo Quoc Thai
    Week 1
    Mario - More
*/
#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int i, j, counter, check, height = 0;
    // Check the input 
    do
    {
        // Get the height from the user input a
        height = get_int("Height: ");
    }
    while (height <= 0 || height >= 9);
    check = height;
    // Start to draw a pyramid
    for (i = height; i >= 1; i--)
    {
        j = 1;
        int temp = check;
        // Fill the gap
        while (j < check)
        {
            printf(" ");
            j++;
            temp--;
        }
        j--;
        counter = 0;
        // Print the # with height - place has been filled with gap
        while (counter < height - j)
        {
            printf("#");
            counter++;	
        }
        printf("  ");
        counter = 0;
        // Print the # with height - place has been filled with gap
        while (counter < height - j)
        {
            printf("#");
            counter++;	
        }
        printf("\n");
        check--;
    }
    return 0;
}
