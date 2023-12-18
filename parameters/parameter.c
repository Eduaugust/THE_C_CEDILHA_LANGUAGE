// result: 5

#include <stdio.h>

void parameter(int a) {
    int b = 3;
    printf("%d\n", a + b);
}

int main() {
    parameter(2);
}

