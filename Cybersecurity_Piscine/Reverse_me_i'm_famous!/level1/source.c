#include <stdio.h>
#include <string.h>

int main(void)
{
    char key[] = "__stack_check";   // copiada a stack en runtime
    char input[100];                // buffer en -0x6c(%ebp)
    //int result = 0;                 // -0x8(%ebp) inicializado a 0

    printf("Please enter key: ");
    scanf("%s", input);

    if (strcmp(input, key) == 0)
        printf("Good job.\n");
    else
        printf("Nope.\n");

    return 0;
}