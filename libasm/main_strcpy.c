#include <stdio.h>
#include <string.h>

extern char *ft_strcpy(char *dst, const char *src);

int main(void) {
    const char src[] = "hola mundo";
    char dst[64];
    char dst_libc[64];

    /* preparar buffers */
    memset(dst, 0x2A, sizeof(dst));      /* llenar con '*' para detectar copia */
    memset(dst_libc, 0x2A, sizeof(dst_libc));

    /* llamar a la función en ensamblador */
    char *ret = ft_strcpy(dst, src);

    /* comparar con strcpy de la libc */
    strcpy(dst_libc, src);

    printf("src:      \"%s\"\n", src);
    printf("dst (asm):\"%s\"\n", dst);
    printf("ret == dst: %s\n", (ret == dst) ? "sí" : "no");
    printf("dst (libc):\"%s\"\n", dst_libc);

    return 0;
}