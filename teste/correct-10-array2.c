// result: sum=0

#include <stdio.h>

int main() {
    int z[10];
    int s = 0;

    int i = 0;
    while (i < 10) {
        s = s + z[i];
        i = i + 1;
    }
    printf("sum=%d\n", s);
}

