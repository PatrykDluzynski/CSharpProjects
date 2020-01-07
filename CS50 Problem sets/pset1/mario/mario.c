#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Create height variable and tell the user the required tower parameters
    int height;
    printf("The height of the tower has to  be between 1 and 8\n");
    // Check for correct user input
    do
    {
        height = get_int("What would you like the height of the tower to be?\n");
    }
    while(height < 1 || height > 8);
    // Iterate through height to print the tower's left side
    for(int i = 0; i < height; i++)
    {
        // Insert spaces first, starting with j = 1
        // j = 1 prevents the printing of extra spaces on the left
        for(int j = 1; j < height - i; j++)
        {
            printf(" ");
        }
        // Print the tower's left side
        for(int k = 0; k <= i; k++)
        {
            printf("#");
        }
        // Make 2 spaces, and print the tower's right side
        printf("  ");
        for(int l = 0; l <= i; l++)
        {
            printf("#");
        }
        printf("\n");
    }

}
