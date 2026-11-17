#include "runtime"
int main(int ac,char **av){
  int k=0;
  int n=0;
  int z=0;
  int r=0;
  char *p=0;
  char *q=(char *)TRANSFER;
  char *check=(char *)INPUT;
  if(ac!=2)return 2;
  k=find(av[1]);
  if(!k)return 1;
  p=bytes(k);
  n=length(k);
  if(u32(p)==EXEZ)return 0;
  if(n<8||u32(p)!=n-4)return 3;
  z=lzencode(p,n,q+4,FILEMAX-4);
  if(z<0||z+4>n)return 4;
  if(lzdecode(q+4,z,check,FILEMAX)!=n||!equal(check,p,n))return 5;
  set32(q,EXEZ);
  if(fsput(av[1],q,z+4))return 6;
  k=find(av[1]);
  r=lzdecode(bytes(k)+4,length(k)-4,(char *)LOADBUF,FILEMAX);
  if(r!=n||!equal(check,(char *)LOADBUF,n))return 7;
  return fscommit();
}

