// semantic errors for arrays

int i = 2;
int a[] = {3, 4};

int a = 0;         // error: 'a' is already declared
int i[] = {0, 0};  // error: 'i' is already declared
int a[] = {0, 0};  // error: 'a' is already declared

a = 0;             // error: array 'a' cannot be changed

i[0] = 0           // error: 'i' is not an array
x[0] = 0           // error: 'x' is not defined

i = a;             // error: array 'a' must be indexed
i = i[0];          // error: variable 'i' cannot be indexed
i = x[0];          // error: 'x' is not defined

