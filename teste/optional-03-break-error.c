// error when using break or continue

#include <stdio.h>

int main() {
    break;  // error: cannot use break outside a loop
    int i = 1;
    while (i <= 10) {
        if (i == 5) {
            break;
        }
        i = i + 1;
    }
}

