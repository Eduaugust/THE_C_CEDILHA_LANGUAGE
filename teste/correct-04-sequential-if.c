// must output 2, 4 and 6

#include <stdio.h>

int main() {
    int x = 77;
    int y = 88;
    if (x == y) {
        printf("%d\n", 1);
    }
    if (x != y) {
        printf("%d\n", 2);
    }
    x = 88;
    if (x < y) {
        printf("%d\n", 3);
    }
    if (x <= y) {
        printf("%d\n", 4);
    }
    if (x > y) {
        printf("%d\n", 5);
    }
    y = 77;
    if (x >= y) {
        printf("%d\n", 6);
    }
}

