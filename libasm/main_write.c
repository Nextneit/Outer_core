#include <stdio.h>
#include <string.h>
#include <unistd.h>

extern ssize_t ft_write(int fd, const void *buf, size_t count);

int main(void) {
    const char *s = "hola desde asm\n";
    ssize_t r = ft_write(-1, s, strlen(s));
    printf("ft_write returned: %zd\n", r);
    return 0;
}