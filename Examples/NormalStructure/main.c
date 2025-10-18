#include "../../StructureMemberOrderChecker.h"

typedef struct
{
    int a;
    int b;
    int c;
    int d;
} test_t;

SMOCHKER(test_t, a, b, c, d);

int main()
{
    return 0;
}
