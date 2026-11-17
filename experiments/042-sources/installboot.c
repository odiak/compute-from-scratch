#include "runtime"
int main(void){
  int k=find("start");
  char *s=0;
  char *t=(char *)(DISK+5120);
  char *d=(char *)(DISK+1024);
  int n=0;
  int i=0;
  if(!k||length(k)>32768)return 1;
  s=bytes(k);
  n=length(k);
  if(u32(s)!=n-4)return 2;
  while(i<n){
    t[i]=s[i];
    i++;
  }
  if(!equal(t,s,n))return 3;
  d[2]=n;
  d[3]=0;
  while(n>255){
    d[3]++;
    n=n-256;
  }
  d[2]=n;
  return fscommit();
}

