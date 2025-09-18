#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
extern ssize_t ft_read(int fd, void *buf, size_t count);

int main(void) {
    char buf[1024];
    /*ssize_t n;

    printf("Introduce texto (ctrl-D para EOF):\n");
    fflush(stdout);

    n = ft_read(0, buf, sizeof(buf));
    if (n < 0) {
        perror("ft_read");
        return 1;
    }

    printf("\nft_read returned: %zd\n--- contenido leído (%zd bytes) ---\n", n, n);
    if (n > 0) {
        ssize_t w = write(1, buf, (size_t)n);
        (void)w;
    }
    printf("\n-----------------------------------\n");*/
    ssize_t r = ft_read(-1, buf, sizeof(buf));
    if (r < 0) {
        printf("ft_read returned: %zd, errno: %d (%s)\n", r, errno, strerror(errno));
    } else {
        printf("ft_read returned: %zd (unexpected success)\n", r);
    }
    return 0;
}