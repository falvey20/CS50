#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{   //Check for Command Line argument
    if (argc == 2)
    {   //Convert String to Integer
        int key = atoi(argv[1]);
        //Store key validity
        bool keyValid = false;
        //Establish if key is Valid
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (isdigit(argv[1][i]))
            {
                keyValid = true;
            }
            else
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }
        if (keyValid == true)
        {
            string plaintext = get_string("plaintext: ");

            for (int i = 0; i < strlen(plaintext); i++)
            {
                if (isupper(plaintext[i]))
                {
                    plaintext[i] = ((plaintext[i] - 65 + key) % 26) + 65;
                }
                else if (islower(plaintext[i]))
                {
                    plaintext[i] = ((plaintext[i] - 97 + key) % 26) + 97;
                }
            }
            printf("ciphertext: %s\n", plaintext);
            return 0;
        }
    }//terminate program
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

}
