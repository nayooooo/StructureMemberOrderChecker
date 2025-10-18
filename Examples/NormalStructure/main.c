#include <stdio.h>
#include "../../StructureMemberOrderChecker.h"

typedef struct
{
    int a;
    int b;
    int c;
    int d;
} test_t;

SMOCHKER(test_t, test_t_order_is_error, a, b, c, d);

int main()
{
    printf("hello checker\n");

    return 0;
}
