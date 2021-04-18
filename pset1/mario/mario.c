#include <stdio.h>
#include <cs50.h>


int main(void)
{
    int towerHeight;
    do {
        towerHeight = get_int("How tall do you want the pyramid?: ");
    }
    while (towerHeight < 1 || towerHeight > 8);
    
    
    for (int row = 0; row < towerHeight; row++)
    {
        for (int dot = 0; dot < towerHeight - row - 1; dot++)
        {
            printf(" ");
        }
        for (int column = 0; column <= row; column++)
        {
            printf("#");
        }
        printf("\n");
    }
    
}
