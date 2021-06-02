#include "a.h"
#include "thing.h"

int main(void)
{
    extern void another(void);
    a();
    another();
}