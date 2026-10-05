#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *ft_strdup(const char *s);

void test_strdup(const char *test_name, const char *input) {
    printf("\n=== %s ===\n", test_name);
    printf("Input: \"%s\"\n", input ? input : "(NULL)");
    
    char *original = strdup(input);
    char *ft_result = ft_strdup(input);
    
    printf("strdup result:    %p -> \"%s\"\n", (void *)original, original ? original : "(NULL)");
    printf("ft_strdup result: %p -> \"%s\"\n", (void *)ft_result, ft_result ? ft_result : "(NULL)");
    
    // Compare results
    if (original == NULL && ft_result == NULL) {
        printf("Both returned NULL\n");
    } else if (original != NULL && ft_result != NULL) {
        if (strcmp(original, ft_result) == 0) {
            printf("Strings match!\n");
        } else {
            printf("Strings differ!\n");
        }
    } else {
        printf("One returned NULL, the other didn't!\n");
    }
    
    // Free memory
    if (original) free(original);
    if (ft_result) free(ft_result);
}

int main(void) {
    printf("Testing ft_strdup function\n");
    printf("================================\n");
    
    // Test cases
    test_strdup("Empty string", "");
    test_strdup("Simple string", "Hello");
    test_strdup("String with spaces", "Hello World");
    test_strdup("Long string", "This is a longer string to test memory allocation");
    test_strdup("Special characters", "!@#$%^&*()_+-=[]{}|;':\",./<>?");
    test_strdup("Numbers", "1234567890");
    test_strdup("Single character", "A");
    test_strdup("Newlines and tabs", "Line1\nLine2\tTabbed");
    
    // Test NULL input (this might cause segfault with standard strdup)
    printf("\n=== NULL input test ===\n");
    printf("Input: (NULL)\n");
    char *ft_null = ft_strdup(NULL);
    printf("ft_strdup result: %p -> \"%s\"\n", (void *)ft_null, ft_null ? ft_null : "(NULL)");
    if (ft_null == NULL) {
        printf("ft_strdup correctly returned NULL for NULL input\n");
    } else {
        printf("ft_strdup should return NULL for NULL input\n");
        free(ft_null);
    }
    
    printf("\nAll tests completed!\n");
    return 0;
}
