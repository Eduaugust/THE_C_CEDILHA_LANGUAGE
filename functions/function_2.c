// result: 88

#include <stdio.h>

int sum(int a, int b) {
    int c = a + b;
    return c;
}

int main() {
    int c = sum(33, 55);
    printf("%d\n", c);
}

