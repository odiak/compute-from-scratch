#include "runtime"
int main(int ac,char **av){
  char *p=(char *)INPUT;
  int n=0;
  int i=0;
  int f=0;
  int done=0;
  int v=31;
  int total=0;
  if(ac==3){
    i=0;
    while(av[2][i]){
      total=total*10+av[2][i]-48;
      i++;
    }
    if(total<0||total>FILEMAX)return 2;
    f=open(av[1],577);
    if(f<0)return 1;
    while(done<total){
      n=total-done;
      if(n>512)n=512;
      i=0;
      while(i<n){
        p[i]=v;
        v=v+17;
        if(v>255)v=v-256;
        i++;
      }
      if(write(f,p,n)!=n)return 1;
      done=done+n;
    }
    return close(f);
  }
  while(1){
    n=read(0,p,512);
    if(n<0)return 1;
    if(!n)break;
    i=0;
    while(i<n){
      if(p[i]==255)p[i]=0;
      else p[i]++;
      i++;
    }
    if(write(1,p,n)!=n)return 1;
  }
  return 0;
}

