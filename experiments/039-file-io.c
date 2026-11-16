#include "libc"
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
int main(){int fd=open("persist",O_WRONLY+O_CREAT+O_TRUNC);int n=0;char *buf=(char *)(16528*256*256+16384);if(fd<0)return 1;if(write(fd,"persistent C file\n",18)!=18)return 2;if(close(fd)<0)return 3;fd=open("persist",O_RDONLY);if(fd<0)return 4;n=read(fd,buf,64);if(n!=18)return 5;if(write(1,buf,n)!=n)return 6;if(read(fd,buf,1)!=0)return 7;if(close(fd)<0)return 8;if(read(fd,buf,1)!=-1||errno!=9)return 9;if(open("nofile",0)!=-1||errno!=2)return 10;fd=open("persist",0);if(write(fd,"X",1)!=-1||errno!=9)return 11;if(close(fd)<0)return 12;if(close(99)!=-1||errno!=9)return 13;return 0;}