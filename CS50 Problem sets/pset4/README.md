# Problem Set 4

This problem set entailed making a program that would detect spelling mistakes in a given text file, by comparing the words against a provided dictionary text file.

Most of the functionality for passing in the words from each file was provided, and the main task was to implement dictionary.c which loaded the dictionary into memory, from the file provided, with my method of choice, print out the size of said dictionary, check against the words passed in, and unload the dictionary from memory without any memory leaks.

I chose to implement the dictionary as a trie.