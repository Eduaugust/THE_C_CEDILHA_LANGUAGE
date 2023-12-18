// results in 1 and 3

#include <stdio.h>

int main() {
    int n = 0;
    while (n <= 5) {
        n = n + 1;
        if (n == 2) {
            continue;
        }
        if (n == 4) {
            break;
        }
        printf("%d\n", n);
    }
}

