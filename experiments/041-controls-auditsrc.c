#include "libc"
int value(char *s){int n=0;while(*s){n=n*10+*s-48;s++;}return n;}
int main(int ac,char **av){char *b=(char *)(16912*256*256);char *d=0;int *h=(int *)b;int f=0;int n=0;int m=0;int k=0;int i=0;if(ac!=4)return 2;f=open(av[1],0);if(f<0)return 2;k=read(f,b,32768);close(f);if(k<8)return 2;n=h[0];if(n<4||n>65532)return 2;m=n+4;if(m>32768)m=32768;if(k!=m)return 2;if(n+4>32768){f=open(av[2],0);if(f<0)return 2;k=read(f,b+32768,32768);close(f);if(k!=n+4-32768)return 2;}d=(char *)value(av[3]);while(i<n){if(d[i]!=b[i+4]){puts("N");return 1;}i++;}puts("Y");return 0;}
