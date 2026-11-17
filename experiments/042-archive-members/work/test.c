#include "runtime"
int main(void){
  char *a=(char *)IMAGE;
  char *saved=(char *)TESTBUF;
  char *cc=saved+FSSIZE;
  char *user=cc+CODEMAX;
  char *p=(char *)INPUT;
  char *c=(char *)COMPILER;
  char *u=(char *)USER;
  int *h=(int *)IMAGE;
  int *d=0;
  int *e=0;
  int i=0;
  int k=0;
  int j=0;
  int r=0;
  int at=0;
  int n=0;
  char *name=(char *)(TRANSFER+FILEMAX+32);
  while(i<FSSIZE){
    saved[i]=a[i];
    i++;
  }
  i=0;
  while(i<CODEMAX){
    cc[i]=c[i];
    user[i]=u[i];
    i++;
  }
  i=0;
  while(i<FSSIZE){
    a[i]=0;
    i++;
  }
  h[0]=MAGIC;
  h[1]=2;
  h[2]=FILES;
  h[3]=FSSIZE;
  h[4]=CODEMAX;
  h[5]=FILEMAX;
  i=0;
  while(i<FILEMAX){
    p[i]=i;
    i++;
  }

  if(fsput("edge",p,FILEMAX)||length(find("edge"))!=FILEMAX||!equal(bytes(find("edge")),p,FILEMAX))r=1;
  if(!fsput("edge",p,FILEMAX+1)||length(find("edge"))!=FILEMAX)r=2;
  if(fsput("other",p,8))r=3;
  d=node(find("edge"));
  e=node(find("other"));
  n=e[2];
  e[2]=d[2];
  if(!fscheck())r=4;
  e[2]=n;
  if(fscheck())r=5;

  name[0]=102;
  name[1]=48;
  name[2]=48;
  name[3]=48;
  name[4]=0;
  i=2;
  while(i<FILES){
    name[3]++;
    if(name[3]>57){
      name[3]=48;
      name[2]++;
    }
    if(fsput(name,p,0))r=6;
    i++;
  }
  if(!fsput("overflow",p,0))r=7;
  i=0;
  while(i<8192){
    ((char *)DIRECTORY)[i]=0;
    i++;
  }
  i=0;
  n=SPACE;while(n){at=n;if(at>FILEMAX)at=FILEMAX;name[3]++;if(fsput(name,p,at))r=8;n=n-at;}
if(!fsput("full",p,1))r=10;

  i=0;
  while(i<8192){
    ((char *)DIRECTORY)[i]=0;
    i++;
  }
  set32(p,5);
  if(fsput("bad",p,9)||native("bad",USER)||native("bad",COMPILER))r=11;
  set32(p,CODEMAX+4);
  if(fsput("bad",p,CODEMAX+8)||native("bad",USER)||native("bad",COMPILER))r=12;
  if(native("bad",COMPILER+4)||native("bad",OUTPUT))r=13;
  set32(p,EXEZ);set32(p+4,8);p[8]=128;p[9]=0;p[10]=0;if(fsput("bad",p,11)||native("bad",USER)||native("bad",COMPILER))r=14;out(1,"capacity result ");
  if(r)putchar(r+64);
  else out(1,"PASS");
  putchar(10);

  i=0;
  while(i<FSSIZE){
    a[i]=saved[i];
    i++;
  }
  i=0;
  while(i<CODEMAX){
    if(cc[i]!=c[i]||user[i]!=u[i])r=20;
    i++;
  }
  out(1,"preservation ");
  if(r)puts("FAIL");
  else puts("PASS");
  return r;
}

