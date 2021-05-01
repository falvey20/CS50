#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 52;

//Hash Index
int hashIndex;

// Hash table
node *table[N];

// Total Word Count
int totalWords = 0;

// Returns true if word is in dictionary else false.
bool check(const char *word)
{
    hashIndex = hash(word); // Get relevant hashIndex for the word.
    node *searcher = table[hashIndex]; // make pointer called searcher to point at the start of the relevant hashIndex.
    while(searcher != NULL) // as long as we don't get to end of linked list
    {
        if(strcasecmp(word, searcher->word) == 0) // strcasecmp(compares string case insensitively). If 
        {
            return true;
        }
        searcher = searcher->next;
    }
    return false;
}

// Hashes word to a number. // Source: djib2 by Dan Bernstein (http://www.cse.yorku.ca/~oz/hash.html)
unsigned int hash(const char *word)
{
unsigned long hash = 5381;
int c = *word;
c = tolower(c);

while (*word != 0)
{
    hash = ((hash << 5) + hash) + c;
    c = *word++;
    c = tolower(c);
}
return hash % N;
}

// Loads dictionary into memory, returning true if successful else false.
bool load(const char *dictionary)
{
    FILE* dictionaryPointer = fopen(dictionary, "r"); // dictionaryPointer points to start of dictionary and prepares to read.
    
    if(dictionaryPointer == NULL) // if dictionaryPointer is NULL return false.
    {
        return false;
    }
    
    char word[LENGTH + 1]; // Initialise word to accept as much as LENGTH(Length is longest word) + 1 for /0.
    
    while (fscanf(dictionaryPointer, "%s", word) != EOF) // While scanning through dictionary does not reach end of file.
    {
        node *nn = malloc(sizeof(node)); // new node(nn) allocates enough memory for the size of node structure(see above).
        if(nn == NULL) // If new node is NULL return false.
        {
            return false;
        }
        strcpy(nn->word, word); // Copy string word into the string word inside the node structure.
        hashIndex = hash(word); // Declare hashNumber as the number given to this word based on hash function.
        nn->next = table[hashIndex]; // Insert node into hash table by using pointer to consecutive nodes.
        table[hashIndex] = nn;
        totalWords++; //Increases the total word count by one.
    }
    
    fclose(dictionaryPointer); // Close dictionary file.
    
    return true; // Return true is succesfully loaded and closed.
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if(totalWords > 0)
    {
        return totalWords;
    }
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {

        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tempCursor = cursor;
            cursor = cursor->next;
            free(tempCursor);
        }
    }
    return true;
}
