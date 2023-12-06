// results in 1000000

#include <stdio.h>

int main() {
    int total = 0;
    int x = 0;
    while (x < 100) {
        int y = 1;
        while (y < 100) {
            total = total + y;
            y = y + 1;
        }
        int z = 100;
        while (z > 0) {
            total = total + z;
            z = z - 1;
        }
        x = x + 1;
    }
    printf("%d\n", total);
}

