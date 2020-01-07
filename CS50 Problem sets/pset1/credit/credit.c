#include <stdio.h>
#include <cs50.h>
#include <math.h>

bool checksum(long n, int len);

int main(void)
{
    // Create number variable and prompt user for input
    long number;
    do
    {
        number = get_long("Number: ");
    }
    while (number < 0);
    
    // Check if at least 13 digits long
    int length_check = 0;
    long check_number = number;
    while (check_number)
    {
        check_number /= 10;
        check_number = floor(check_number);
        length_check++;
    }
    
    // If the check passes, check the possible maufacturers
    if (length_check >= 13)
    {
        // Initialize a variable for the first number
        // Keep dividing by 10 to get the first number
        long first_number = number;
        while (first_number > 100)
        {
            first_number /= 10;
        }
        // If the first number is 3 or 4 or 5 we can deduce the manufacturers
        // Checking the first number along with the length will pinpoint the manufacturer
        // If the checksum is also valid we can print the manufacturer's name
        if ((first_number == 34 || first_number == 37) && length_check == 15)
        {
            if (checksum(number, length_check))
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (first_number/10 == 4 && (length_check == 13 || length_check == 16))
        {
            if (checksum(number, length_check))
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if ((first_number == 51 || first_number == 52 || first_number == 53 || first_number == 54 || first_number == 55) && length_check == 16)
        {
            if (checksum(number, length_check))
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

// Define the checksum function
bool checksum(long n, int len)
{
    // Create the required variables and arrays
    long num = n;
    long phase1[8];
    long phase2[16];
    long phase3[8];
    int sum = 0;
    // Loop through the number, starting with the last digit
    // Assign the last to array used in phase 3
    // Assign 2nd last to array ued in phase 1 and 2
    // Keep going and alternating between numbers
    for (int i = 0; i < 8; i++)
    {
        phase3[i] = num % 10;
        num /= 10;
        phase1[i] = num % 10;
        num /= 10;
    }
    // Multiply each number in array 1 by 2, and assign each digit to a position in array 2
    for (int i = 0; i < (sizeof(phase1) / sizeof(phase1[0])); i++)
    {
        int k = phase1[i] * 2;
        phase2[i * 2] = k % 10;
        k /= 10;
        phase2[(i * 2) + 1] = k % 10;
    }
    // Add each digit in array 2 to the sum
    for (int i = 0; i < 16; i++)
    {
        sum += phase2[i];
    }
    // Add each digit in array 3 to the sum
    for (int i = 0; i < 8; i++)
    {
        sum += phase3[i];
    }
    // Check if the sum is divisible evenly by 10
    if (sum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
