// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: resize n infile outfile\n");
        return 1;
    }

    if (atoi(argv[1]) > 100 || atoi(argv[1]) < 1)
    {
        fprintf(stderr, "Usage: n should be between 1 and 100 inclusive\n");
        return 1;
    }

    // remember filenames and size specified
    int size = atoi(argv[1]);
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // determine padding for scanlines
    int paddingold = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // save old height and width
    int biHeightold = abs(bi.biHeight);
    int biWidthold = bi.biWidth;

    // set new height and width
    bi.biWidth *= size;
    bi.biHeight *= size;

    // determine padding for the new parameters
    int paddingnew = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // Calculate new biSizeImage
    bi.biSizeImage = ((bi.biWidth * sizeof(RGBTRIPLE)) + paddingnew) * abs(bi.biHeight);

    // Calculate new bfSize
    bf.bfSize = bi.biSizeImage + 54;

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    // iterate over infile's scanlines
    for (int i = 0; i < biHeightold; i++)
    {
        for (int l = 0; l < (size - 1); l++)
        {
            // iterate over pixels in scanline
            for (int j = 0; j < biWidthold; j++)
            {
                // temporary storage of rgbtriple
                RGBTRIPLE triple;

                // read RGB triple from infile
                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                for (int k = 0; k < size; k++)
                {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
                }
            }

            // add padding if any
            for (int m = 0; m < paddingnew; m++)
            {
                fputc(0x00, outptr);
            }

            fseek(inptr, -(biWidthold * sizeof(RGBTRIPLE)), SEEK_CUR);
        }

        for (int j = 0; j < biWidthold; j++)
        {
            // temporary storage of rgbtriple
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            for (int k = 0; k < size; k++)
            {
                    fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
        }

        // add padding if any
        for (int m = 0; m < paddingnew; m++)
        {
                fputc(0x00, outptr);
        }
        // skip over padding, if any
        fseek(inptr, paddingold, SEEK_CUR);

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}
