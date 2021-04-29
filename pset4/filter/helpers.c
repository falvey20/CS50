#include "helpers.h"
#include <stdio.h>
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int red = image[i][j].rgbtRed;

            float avgRGB = round((round(red) + round(green) + round(blue)) / 3);

            image[i][j].rgbtBlue = avgRGB;
            image[i][j].rgbtGreen = avgRGB;
            image[i][j].rgbtRed = avgRGB;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
     for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < width; j++)
        {
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int red = image[i][j].rgbtRed;

            int sepiaRed = round(.393 * red + .769 * green + .189 * blue);
            if(sepiaRed > 255)
                {
                    image[i][j].rgbtRed = 255;
                }
                else
                {
                    image[i][j].rgbtRed = sepiaRed;
                }
            int sepiaBlue = round(.272 * red + .534 * green + .131 * blue);
            if(sepiaBlue > 255)
                {
                    image[i][j].rgbtBlue = 255;
                }
                else
                {
                    image[i][j].rgbtBlue = sepiaBlue;
                }
            int sepiaGreen = round(.349 * red + .686 * green + .168 * blue);
            if(sepiaGreen > 255)
                {
                    image[i][j].rgbtGreen = 255;
                }
                else
                {
                    image[i][j].rgbtGreen = sepiaGreen;
                }
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for(int i = 0; i < height; i++)
    {
        for(int j = 0; j < (width/2); j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copyOfImage[height][width];
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = 0;
            int green = 0;
            int blue = 0;
            float totalPixels = 0.00;

            //Rows around pixel
            for (int r = -1; r < 2; r++)
            {
                //Columns around pixel
                for (int c = -1; c < 2; c++)
                {
                    // If current row + next row are within bounds
                    // If current column + next column are within bounds
                    if(i + r < 0 || i + r > height - 1 || j + c < 0 || j + c > width - 1)
                    {
                        continue;
                    }

                        red += image[i + r][j + c].rgbtRed;
                        green += image[i + r][j + c].rgbtGreen;
                        blue += image[i + r][j + c].rgbtBlue;

                        totalPixels++;
                    }
                }
            copyOfImage[i][j].rgbtRed = round(red / totalPixels);
            copyOfImage[i][j].rgbtGreen = round(green / totalPixels);
            copyOfImage[i][j].rgbtBlue = round(blue / totalPixels);
            
            }
            
        }
        for(int i = 0; i < height; i++)
        {
            for(int j = 0; j < width; j++)
            {
                image[i][j].rgbtRed = copyOfImage[i][j].rgbtRed;
                image[i][j].rgbtGreen = copyOfImage[i][j].rgbtGreen;
                image[i][j].rgbtBlue = copyOfImage[i][j].rgbtBlue;
            }
        }
        
        return;
    }

