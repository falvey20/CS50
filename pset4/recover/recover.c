#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>


int main(int argc, char *argv[])
{
    
// Check for correct input and return 1 if incorrect.
    if(argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
// argv[1] represented as a string of characters (filename).    
    char *inputFile = argv[1];
// Open file at input pointer.    
    FILE *inputPointer = fopen(inputFile, "r");
// If file is NULL return 1 and error message.
    if(inputFile == NULL)
    {
        printf("Can not open %s\n", inputFile);
        return 1;
    }
// Create a buffer and read 512 bytes into buffer, if start of new jpeg write new jpeg, otherwise close current file and open new file.
typedef uint8_t BYTE;
BYTE buffer[512]; // buffer of 512 BYTES
int jpgCount = 0;
bool jpgFound = false;
FILE *outputPointer = NULL;

//Go through all chunks of 512 Bytes and if a jpg is recognised write a new jpg file.
while(fread(buffer, 512, 1, inputPointer) > 0)
  {
    if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) // Using provided bitwise operator.
    {
      if(jpgFound == true) // If this jpg has already been found close the output pointer
      {
        fclose(outputPointer);
      }
      else // Otherwise I know this is a new jpg so declare as true
        {
          jpgFound = true;
        }
      char filename[8]; // Allocates 8 characters for 000.jpeg\0
      sprintf(filename, "%03i.jpg", jpgCount); // Prints jpgCount to filename in correct format
      jpgCount++;
      outputPointer = fopen(filename, "w"); // Output pointer writes to jpg file
    }
    
    if(jpgFound == true) // If it is a jpeg and above has not dictated that it's new, continue to write from the buffer to the output pointer
    {
       fwrite(buffer, 512, 1, outputPointer); // Write new jpg
    }
    
  }
  
}

//14. end of memory card
//15. close all open files
