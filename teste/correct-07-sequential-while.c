// results in 1, 2, 3, 2 and 1

#include <stdio.h>

int main() {
    int n = 1;
    while (n <= 2) {
        printf("%d\n", n);
        n = n + 1;
    }
    while (n >= 1) {
        printf("%d\n", n);
        n = n - 1;
    }
}
