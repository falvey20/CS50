#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include<math.h>

int main(void)
{
    //Ask for text
    string providedText = get_string("Text: \n");
    int numOfCharacters = strlen(providedText);

    int actualWords = 1;
    int actualLetters = 0;
    int actualSentences = 0;
    
    for (int i = 0; i <= numOfCharacters; i++)
    {
        if (isalpha(providedText[i]))
        {
            actualLetters += 1;
        }
        else if (isspace(providedText[i]))
        {
            actualWords += 1;
        }
        else if (providedText[i] == '.' || providedText[i] == '?' || providedText[i] == '!')
        {
            actualSentences += 1;
        }
        else
        {
            actualLetters += 0;
            actualWords += 0;
            actualSentences += 0;
        }
    }
    //printf("Letters in text: %i\n", actualLetters);
    //printf("Words in text: %i\n", actualWords);
    //printf("Sentences in text: %i\n", actualSentences);
    int colemanLiauIndex = round(0.0588 * ((float)actualLetters / actualWords * 100) - 0.296 * ((float)actualSentences / actualWords * 100) - 15.8);
    if (colemanLiauIndex >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (colemanLiauIndex < 1) 
    {
        printf("Before Grade 1\n");
    }
    else 
    {
        printf("Grade %i\n", colemanLiauIndex);
    }
    
}


//index = 0.0588 * L - 0.296 * S - 15.8    Coleman Liau Index




