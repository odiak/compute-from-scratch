/* Exercise C semantics independently of the upstream command. */
int main(int argc, char *argv[])
{
    int n = 0;
    int value = 37;
    int *p = &value;
    char **next = argv + 1;

    if (0 && n++)
        return 1;
    if (!(1 || n++))
        return 2;
    if (n != 0)
        return 3;
    if ((1 && ++n) != 1)
        return 4;
    if ((0 || ++n) != 1)
        return 5;
    if (n != 2)
        return 6;
    if (next - argv != 1 || (1 + argv) != next)
        return 7;
    if (argc > 1 && *next != argv[1])
        return 8;
    if ((p + 1) - p != 1 || *(p + 0) != 37)
        return 9;
    if ((0 ? n++ : ++n) != 3)
        return 10;
    if ((1 ? ++n : n++) != 4)
        return 11;
    for (n = 0; n < 4; n++)
        value += n;
    if (value != 43)
        return 12;
    n = (value++, value - 40);
    if (n != 4 || value != 44)
        return 13;
    return 0;
}
