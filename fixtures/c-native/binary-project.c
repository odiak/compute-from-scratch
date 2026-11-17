#include "runtime"
#include "bits"
/* Ordinary C project using the environment's generic 32-bit bit operations. */
int probe_number(char *text) {
    int result = 0;
    while (*text) {
        if (*text < 48 || *text > 57) return 0-1;
        result = result*10 + *text-48;
        text++;
    }
    return result;
}
int main(int argc, char **argv) {
    char *buffer = (char *)TESTBUF;
    int count = 0;
    int at = 0;
    int done = 0;
    int size = 0;
    int state = 0;
    if (argc > 1 && !strcmp(argv[1], "exit")) {
        out(2, "nested exit\n");
        exit(7);
    }
    if (argc == 4 && !strcmp(argv[1], "generate")) {
        size = probe_number(argv[2]);
        state = probe_number(argv[3]);
        if (size < 0 || size > FILEMAX || state < 1) return 2;
        bitinit();
        while (done < size) {
            count = size-done;
            if (count > 4096) count = 4096;
            at = 0;
            while (at < count) {
                state = bx(state, bit(1, bit(4, state, 19), 0-8192));
                state = bx(state, bit(3, state, 17));
                state = bx(state, bit(1, bit(4, state, 27), 0-32));
                buffer[at] = state;
                at++;
            }
            if (write(1, buffer, count) != count) return 8;
            done = done+count;
        }
        return 0;
    }
    while ((count = read(0, buffer, 4096)) > 0) {
        at = 0;
        while (at < count) {
            if (buffer[at] > 96 && buffer[at] < 123)
                buffer[at] = buffer[at] - 32;
            at++;
        }
        if (write(1, buffer, count) != count) return 8;
    }
    return count < 0;
}
