// warning for unused variables

#include <stdio.h>

int main() {
    int a = 2;
    int b = a * 3;
    int c = 4;
    printf("%d\n", a);

    // warning: 'b' is defined but never used
    // warning: 'c' is defined but never used
}

// symbol_table: ['a', 'b', 'c']
// used_vars: [True, False, False]

