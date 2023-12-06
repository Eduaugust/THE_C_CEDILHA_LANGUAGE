// must output 7

#include <stdio.h>

int main() {
    int a = 1;
    int b = 2;
    int c = 3;
    if (a == b) {
        if (b > c) {
            printf("%d\n", 4);
        }
        if (b <= c) {
            printf("%d\n", 5);
        }
    }
    if (a != b) {
        if (a < b) {
            if (b > c) {
                printf("%d\n", 6);
            }
            if (b <= c) {
                printf("%d\n", 7);
            }
        }
        if (a >= b) {
            printf("%d\n", 8);
        }
    }
}

