#include "libc"
int square(int x){return x*x;}
int main(int ac,char **av){
if(ac>1){char *b=(char *)(16624*256*256+1024*256);int i=0;int n=0;
if(!strcmp(av[1],"binary")){b[0]=65;b[1]=0;b[2]=4;b[3]=66;b[4]=10;return write(1,b,5)!=5;}
if(!strcmp(av[1],"count")){while((i=read(0,b,256))>0)n=n+i;return i<0||n!=32768;}
while(i<32768){b[i]=65;i++;}if(write(1,b,32768)!=32768)return 7;
if(!strcmp(av[1],"overflow")&&write(1,b,1)!=1){out(2,"capacity rejected\n");return 7;}return 0;}
puts("orbit area: sixteen");
return square(4)!=16;
}
