#include <stdio.h>
#include <math.h>
#include <cs50.h>

int main(void)
{
    float totalChange;

    do 
    {
        totalChange = get_float("How much change is owed?: \n");
    } while (totalChange < 0);
    
    
    int cents = round(totalChange * 100);
    int coins = 0;
    
   while (cents >= 25) {
       cents -= 25;
       coins++;
   } while (cents >= 10) {
       cents -= 10;
       coins++;
   } while (cents >= 5) {
       cents -= 5;
       coins++;
   } while (cents >= 1) {
       cents -= 1;
       coins++;
   }

    printf("%i\n",coins);
}
