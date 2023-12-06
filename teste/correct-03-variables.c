// expected: 10, 8 and 6

#include <stdio.h>

int main() {
    int x = 2;
    printf("%d\n", x * 5);
    int y = x / 2;
    printf("%d\n", 4 + x * (3 - y));
    x = 6;
    printf("%d\n", x);
}

// symbol_table: ['x', 'y']

