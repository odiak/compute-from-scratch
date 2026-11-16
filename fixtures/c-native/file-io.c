#include "libc"
#include <fcntl.h>

/* The harness supplies a writable argv buffer of at least 32 bytes. */
int main(int argc, char **argv)
{
    char *buffer;
    char *contents = "A\0Z\n";
    int fd;
    int length;

    if (argc != 3)
        return 90;
    if (strlen(argv[2]) < 32)
        return 91;
    buffer = argv[2];
    fd = open(argv[1], O_WRONLY + O_CREAT + O_TRUNC);
    if (fd < 0)
        return 1;
    if (write(fd, contents, 4) != 4)
        return 2;
    if (close(fd))
        return 3;

    fd = open(argv[1], O_RDONLY);
    if (fd < 0)
        return 4;
    length = read(fd, buffer, 32);
    if (length != 4)
        return 5;
    if (read(fd, buffer + 4, 1))
        return 6;
    if (write(fd, contents, 1) + 1)
        return 7;
    if (close(fd))
        return 8;
    if (write(1, buffer, 4) != 4)
        return 9;
    return 0;
}
