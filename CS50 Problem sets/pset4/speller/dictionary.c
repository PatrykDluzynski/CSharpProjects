// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents number of children for each node in a trie
#define N 27

// Represents a node in a trie
typedef struct node
{
    bool is_word;
    struct node *children[N];
}
node;
// Represents a trie
node *root;

int charcon(char c);
void wordcount(node *ptr, int *counter, int num);
void freemem(node *ptr, int num);

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    root = malloc(sizeof(node));
    if (root == NULL)
    {
        return false;
    }
    root->is_word = false;
    for (int i = 0; i < N; i++)
    {
        root->children[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into trie
    while (fscanf(file, "%s", word) != EOF)
    {
        // Define a crawl pointer to "crawl" through the trie
        node *crawl = root;

        for (int i = 0; i < strlen(word); i++)
        {
            // Define ind to convert each letter of the word, into its corresponding alphabet index
            int ind = charcon(word[i]);

            // If there is nothing at the children index at the node we are currently pointing to, then we create a new node at that children index
            if (crawl->children[ind] == NULL)
            {
                // We malloc memory of the size of a node at the children index
                crawl->children[ind] = malloc(sizeof(node));
                if (crawl->children[ind] == NULL)
                {
                    return false;
                }
                // We indicate that it is not the end of a word
                crawl->children[ind]->is_word = false;
                // Each child within the newly allocated node is then initialised to null
                for (int j = 0; j < N; j++)
                {
                    crawl->children[ind]->children[j] = NULL;
                }
            }
            // crawl then points towards the existing node in the trie
            crawl = crawl->children[ind];
        }
        // Once the entire word has been allocated the last node which we point to, is marked as a leaf (is_word = true)
        crawl->is_word = true;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    int wordnum = 0;
    int *ptr = &wordnum;
    node *crawl = root;
    wordcount(crawl, ptr, N);
    return wordnum;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Define a len variable to store the length of the word
    int len = strlen(word);
    // Define a crawl pointer to "crawl" through the trie
    node *crawl = root;

    for (int i = 0; i < len; i++)
    {
        // Define ind to convert each letter of the word, into its corresponding alphabet index
        int ind = charcon(word[i]);

        // If there is nothing at the children index at the node we are currently pointing to, then we return false
        if (!crawl->children[ind])
        {
            return false;
        }

        crawl = crawl->children[ind];
    }
    // At the end we check if the node we point to is not NULL, and if it's the end of a word
    if (crawl != NULL && crawl->is_word == true)
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    freemem(root, N);
    return true;
}

// Define a function for converting letters into their respective index
int charcon(char c)
{
    int index;
    if (c == '\'')
    {
        index = 26;
        return index;
    }
    else if (c >= 'A' && c <= 'Z')
    {
        index = c - 'A';
        return index;
    }
    else if (c >= 'a' && c <= 'z')
    {
        index = c - 'a';
        return index;
    }
    else
    {
        printf("Encountered an unexpected character, exiting...\n");
        exit(1);
    }
}

void wordcount(node *ptr, int *counter, int num)
{
    for (int i = 0; i < num; i++)
    {
        if (ptr->children[i] != NULL)
        {
            node *newptr = ptr->children[i];
            wordcount(newptr, counter, num);
        }
    }
    if (ptr != NULL && ptr->is_word == true)
    {
        *counter += 1;
    }
}

void freemem(node *ptr, int num)
{
    for (int i = 0; i < num; i++)
    {
        if (ptr->children[i] != NULL)
        {
            node *newptr = ptr->children[i];
            freemem(newptr, num);
        }
    }
    free(ptr);
}