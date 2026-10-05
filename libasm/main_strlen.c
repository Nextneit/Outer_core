#include <stdio.h>
#include <stddef.h>
#include <string.h>

extern size_t ft_strlen(const char *s);

int main(void) {
    const char *tests[] = {"", "a", "hola mundo", "cadena con espacios", "una\0otra"};
    for (int i = 0; i < 5; ++i){
        printf("String number %i\n", i);
        printf("Size of string number in ft_strlen -> %zu\n", ft_strlen(tests[i]));
        printf("Size of string number in strlen -> %zu\n", strlen(tests[i]));
    }

    return 0;
}