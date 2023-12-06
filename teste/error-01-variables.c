#include <stdio.h>

int main() {
    a = 1;     // error: variable 'a' not declared

    int b = 2;
    int b = 3; // error: cannot redeclare variable 'b'

    int x = 1 + 2 * c - 3;  // error: unknown variable 'c'

    printf("%d\n", d);      // error: unknown variable 'd'
}

