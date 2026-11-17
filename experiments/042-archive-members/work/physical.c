#include "runtime"
#include "bits"
int main(void){
  char *image=(char *)IMAGE;
  char *save=(char *)TESTBUF;
  char *old=(char *)TRANSFER;
  char *disk=(char *)DISK;
  char *p=(char *)INPUT;
  char *name=(char *)(EDITBUF+FILEMAX+32768);
  int *h=(int *)IMAGE;
  int i=0;
  int left=SPACE;
  int size=0;
  int r=0;
  int v=31;
  bitinit();
  while(i<FSSIZE){
    save[i]=image[i];
    i++;
  }
  i=1024;
  while(i<16*256*256){
    old[i]=disk[i];
    i++;
  }
  i=0;
  while(i<FSSIZE){
    image[i]=0;
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
    v=bit(1,v*25173+13849,(65534+1));
    p[i]=bit(3,v,8);
    i++;
  }
  name[0]=120;
  name[1]=48;
  name[2]=0;
  while(left){
    size=left;
    if(size>FILEMAX)size=FILEMAX;
    name[1]++;
    if(fsput(name,p,size))r=1;
    left=left-size;
  }
  if(fscommit()!=3)r=2;
  if(!equal(old+1024,disk+1024,16*256*256-1024))r=3;
  i=0;
  while(i<FSSIZE){
    image[i]=save[i];
    i++;
  }
  if(fscommit())r=4;
  if(r)puts("physical capacity FAIL");
  else puts("incompressible physical-capacity failure preserves every cached disk byte PASS");
  return r;
}

