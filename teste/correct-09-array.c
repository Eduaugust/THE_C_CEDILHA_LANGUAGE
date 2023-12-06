// result: 25 16 9 4 1

#include <stdio.h>

int main() {
    int v[] = {1, 2, 3, 4, 5};
    int n = 5;

    int i = 0;
    while (i < n) {
        v[i] = v[i] * v[i];
        i = i + 1;
    }

    i = n - 1;
    while (i >= 0) {
        printf("%d\n", v[i]);
        i = i - 1;
    }
}

