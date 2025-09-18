#include <stdio.h>
#include <stddef.h>

extern size_t ft_strlen(const char *s);

int main(void) {
    const char *tests[] = {"", "a", "hola mundo", "cadena con espacios", "una\0otra"};
    for (int i = 0; i < 5; ++i)
        printf("Size of string number %d -> %zu\n", i, ft_strlen(tests[i]));
    return 0;
}