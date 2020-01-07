#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

// Declare functions used
bool digitcheck(string x);
void shift(string input, int key);

int main(int argc, string argv[])
{
    // Check number of args
    if (argc == 2)
    {
        // Check if argument given is in digits only
        if (digitcheck(argv[1]))
        {
            string s = get_string("plaintext: ");
            shift(s, atoi(argv[1]));
            return 0;
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}

// Define a function for digit checking
bool digitcheck(string x)
{
    // Initialize an int for checking number of digits in the argument, and length of argument
    int checknum = 0;
    int n = strlen(x);
    
    // Iterate through each element of argument string
    for (int i = 0; i < n; i++)
    {
        // Check if each character is a digit
        if (isdigit(x[i]))
        {
            checknum++;
        }
        else
        {
            checknum += 0;
        }
    }
    // If the checknumber is the same as the number of characters, that means all characters are digits
    if (checknum == n)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Define a function for shifting
void shift(string input, int key)
{
    printf("ciphertext: ");
    // Iterate through each of the chars in the input
    for (int i = 0, n = strlen(input); i < n; i++)
    {
        // We want to "normalize" the position of the alphabet in our program to 0 - 25 where a is 0 and z is 25
        // Capitals and lowercase letters have different positions
        // By subtracting the start of the respective upper or lowercase alphabet, we can shift the input to 0 - 25
        // We then add the key, and take the modulo in case the key pushes the input past the end of the alphabet
        // By adding the start of the respective alphabet again, we print the shifted letter correctly
        // If the character is not a letter it gets reprinted as it is
        if (input[i] >= 'A' && input[i] <= 'Z')
        {
            printf("%c", ((input[i] - 'A' + key) % 26) + 'A');
        }
        else if (input[i] >= 'a' && input[i] <= 'z')
        {
            printf("%c", ((input[i] - 'a' + key) % 26) + 'a');
        }
        else
        {
            printf("%c", input[i]);
        }
    }
    printf("\n");
}
