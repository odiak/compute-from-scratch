/* Ordinary directives, including an empty include guard and a continued macro. */
#define BASE 3
#define TOTAL (BASE + \
4)

#ifndef GUARD
#define GUARD
#ifdef NEVER_DEFINED
char *not_a_directive = "#endif inside a string";
these tokens must be discarded;
#else
int chosen(void)
{
    return TOTAL;
}
#endif
#else
these tokens must also be discarded;
#endif

int main(void)
{
    char *literal = "TOTAL #endif";
    if (literal[0] != 'T')
        return 1;
    return chosen() != 7;
}
