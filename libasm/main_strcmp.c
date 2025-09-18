#include <stdio.h>
#include <string.h>
#include <limits.h>

extern int ft_strcmp(const char *s1, const char *s2);

static const char *show(const char *s) { return s ? s : "(NULL)"; }

int main(void) {
    const char *tests[][2] = {
        {"", ""},
        {"a", "a"},
        {"abc", "abd"},
        {"hola", "hola mundo"},
        {"hola mundo", "hola"},
        {NULL, NULL},
        {"", NULL},
        {NULL, ""}
    };

    for (size_t i = 0; i < sizeof(tests)/sizeof(tests[0]); ++i) {
        const char *a = tests[i][0];
        const char *b = tests[i][1];
        int res_asm = ft_strcmp(a, b);
        int res_lib = INT_MIN; /* marcador si no se puede llamar a strcmp */
        if (a && b) res_lib = strcmp(a, b);

        printf("test %zu: a=%s, b=%s\n", i, show(a), show(b));
        printf("  ft_strcmp -> %d\n", res_asm);
        if (res_lib != INT_MIN)
            printf("  strcmp    -> %d\n", res_lib);
        else
            printf("  strcmp    -> (no se llama con NULL)\n");
        printf("  signo asm: %d, signo libc: %s\n\n",
               (res_asm>0) - (res_asm<0),
               (res_lib==INT_MIN) ? "(n/a)" :
               ((res_lib>0) ? "positivo" : (res_lib<0) ? "negativo" : "cero"));
    }

    return 0;
}