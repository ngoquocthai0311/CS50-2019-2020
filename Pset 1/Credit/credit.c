/*
 * Ngo Quoc Thai
 * Week 1
 * Credit.c
*/
#include <stdio.h>
#include <cs50.h>
#include <math.h>
int main(void)
{
    long num_replica;
    int last_digit, sum = 0, length = 0;
    long num = get_long("Number: ");
    num_replica = num;
    last_digit = num % 10;
    num_replica /= 10;
    // Devide the number untill it reaches 0
    while (num_replica != 0)
    {
        // Each digit taken multypli by 2
        int temp_digit = (num_replica % 10) * 2;
        // If the product is larger or equal to 10
        if (temp_digit >= 10)
        {
            // Divide it into digit and add it to the sum
            while (temp_digit != 0)
            {
                sum += temp_digit % 10;
                temp_digit /= 10;
            }
        } 
        else 
        {
            sum += temp_digit;
        }
        length++;
        num_replica /= 100;
    }
    num_replica = num;
    // Add remain number which is not multiplied by 2 
    while (num_replica != 0)
    {
        sum += num_replica % 10;
        length++;
        num_replica /= 100;
    }
    if (sum % 10 == 0 && length >= 13)
    {
        int check_type = num / pow(10, length - 2);
        int check_visa = num / pow(10, length - 1);
        // Check the type with starting numbers
        switch (check_type)
        {
            case 51:
            case 52:
            case 53:
            case 54:
            case 55:
                printf("MASTERCARD\n");
                break;
            case 34:
            case 37:
                printf("AMEX\n");
                break;
            default:
                if (check_visa == 4)
                {
                    printf("VISA\n");
                } 
                else
                {
                    printf("INVALID\n");   
                }
                break;
        }
    } 
    else
    {
        printf("INVALID\n");
    }
    return 0;
}
