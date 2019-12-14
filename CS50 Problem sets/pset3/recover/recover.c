#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    typedef uint8_t  BYTE;

    // Ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // Remember infile
    char *infile = argv[1];

    // Open the input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Error, the file could not be read.\n");
        return 2;
    }

    // Initialize a counter for filenames
    int counter = 0;
    char *filename = malloc(8 * sizeof(char));

    sprintf(filename, "%03i.jpg", counter);
    FILE *outptr;

    // Define a bool to check if a file is already open
    bool fileopen = false;

    // Define a temporary buffer
    BYTE buffer[512];

    // While whole 512 blocks are read, keep reading 512 blocks
    while (fread(buffer, sizeof(BYTE), 512, inptr) == 512)
    {
        // Since data was read to check if it's valid, we need to go back 512 bytes if it is indeed valid
        fseek(inptr, -512 * sizeof(BYTE), SEEK_CUR);

        // Read a 512 byte block and save it in a temporary buffer
        fread(buffer, sizeof(BYTE), 512, inptr);

        // If start of file was found
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If there is a file already open, close it, and increase counter by 1
            if (fileopen == true)
            {
                fclose(outptr);
                counter++;
            }

            // Change name of file to match counter
            sprintf(filename, "%03i.jpg", counter);
            // Open new file
            outptr = fopen(filename, "w");
            // Write to new file
            fwrite(buffer, sizeof(BYTE) * 512, 1, outptr);
            // Change bool to indicate there is now a file open
            fileopen = true;
        }
        // If a file is open, write to it (this is mainly used as a failsafe for the first few chunks of data, where no files are present)
        else if (fileopen == true)
        {
            fwrite(buffer, sizeof(BYTE) * 512, 1, outptr);
        }
    }

    fclose(inptr);
    fclose(outptr);
    free(filename);

    return 0;
}
