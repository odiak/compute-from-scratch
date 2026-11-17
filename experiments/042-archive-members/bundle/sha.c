#include "runtime"
#include "bits"
int hv(int c){
  if(c>96)return c-87;
  return c-48;
}

int constants(char *s,int *p,int n){
  int i=0;
  int j=0;
  int v=0;
  while(i<n){
    v=0;
    j=0;
    while(j<8){
      v=v*16+hv(*s);
      s++;
      j++;
    }
    p[i]=v;
    i++;
  }
  return 0;
}

int block(char *p){
  int *w=(int *)SHASTATE;
  int *k=w+80;
  int *h=w+160;
  int i=0;
  int a=0;
  int b=0;
  int c=0;
  int d=0;
  int e=0;
  int f=0;
  int g=0;
  int v=0;
  int x=0;
  int y=0;
  int t=0;
  int u=0;
  while(i<16){
    w[i]=p[0]*256*256*256+p[1]*256*256+p[2]*256+p[3];
    p=p+4;
    i++;
  }
  while(i<64){
    a=w[i-15];
    b=w[i-2];
    x=bx(bx(bit(4,a,7),bit(4,a,18)),bit(3,a,3));
    y=bx(bx(bit(4,b,17),bit(4,b,19)),bit(3,b,10));
    w[i]=w[i-16]+x+w[i-7]+y;
    i++;
  }
  a=h[0];
  b=h[1];
  c=h[2];
  d=h[3];
  e=h[4];
  f=h[5];
  g=h[6];
  v=h[7];
  i=0;
  while(i<64){
    x=bx(bx(bit(4,e,6),bit(4,e,11)),bit(4,e,25));
    y=bx(bit(1,e,f),bit(1,bx(e,0-1),g));
    t=v+x+y+k[i]+w[i];
    x=bx(bx(bit(4,a,2),bit(4,a,13)),bit(4,a,22));
    y=bx(bx(bit(1,a,b),bit(1,a,c)),bit(1,b,c));
    u=x+y;
    v=g;
    g=f;
    f=e;
    e=d+t;
    d=c;
    c=b;
    b=a;
    a=t+u;
    i++;
  }
  h[0]=h[0]+a;
  h[1]=h[1]+b;
  h[2]=h[2]+c;
  h[3]=h[3]+d;
  h[4]=h[4]+e;
  h[5]=h[5]+f;
  h[6]=h[6]+g;
  h[7]=h[7]+v;
  return 0;
}

int hx(int c){
  int q=0;
  while(c>15){
    q++;
    c=c-16;
  }
  if(q>9)putchar(q+87);
  else putchar(q+48);
  if(c>9)putchar(c+87);
  else putchar(c+48);
  return 0;
}

int dec(int n){
  int q=0;
  while(n>9){
    n=n-10;
    q++;
  }
  if(q)dec(q);
  putchar(n+48);
  return 0;
}

int digest(char *p,int n){
  int *w=(int *)SHASTATE;
  int *h=w+160;
  int i=n;
  int total=0;
  int j=0;
  int len=n*8;
  constants("6a09e667bb67ae853c6ef372a54ff53a510e527f9b05688c1f83d9ab5be0cd19",h,8);
  while(total<n+9)total=total+64;
  p[i]=128;
  i++;
  while(i<total){
    p[i]=0;
    i++;
  }
  p[total-4]=bit(3,len,24);
  p[total-3]=bit(3,len,16);
  p[total-2]=bit(3,len,8);
  p[total-1]=len;
  i=0;
  while(i<total){
    block(p+i);
    i=i+64;
  }
  i=0;
  while(i<8){
    j=24;
    while(j>0-1){
      hx(bit(1,bit(3,h[i],j),255));
      j=j-8;
    }
    i++;
  }
  return 0;
}

int inventory(char *b,int n){
  char *p=(char *)(SHABUF+FILEMAX+4096);
  int at=0;
  int z=0;
  int len=0;
  int i=0;
  if(n<1)return 2;
  while(at<n&&b[at]){
    z=b[at];
    if(z>NAMEMAX||at+3+z>n)return 2;
    len=b[at+1]+b[at+2]*256;
    if(at+3+z+len>n)return 2;
    i=0;
    while(i<len){
      p[i]=b[at+3+z+i];
      i++;
    }
    digest(p,len);
    out(1,"  ");
    write(1,b+at+3,z);
    putchar(32);
    dec(len);
    putchar(10);
    at=at+3+z+len;
  }
  if(at!=n-1||b[at])return 2;
  return 0;
}

int value(char *s){
  int n=0;
  while(*s){
    if(*s<48||*s>57)return -1;
    n=n*10+*s-48;
    s++;
  }
  return n;
}

int main(int ac,char **av){
  char *b=(char *)SHABUF;
  int *k=(int *)(SHASTATE+320);
  int i=1;
  int f=0;
  int n=0;
  int addr=0;
  int j=0;
  char *mem=0;
  bitinit();
  constants("428a2f9871374491b5c0fbcfe9b5dba53956c25b59f111f1923f82a4ab1c5ed5d807aa9812835b01243185be550c7dc372be5d7480deb1fe9bdc06a7c19bf174e49b69c1efbe47860fc19dc6240ca1cc2de92c6f4a7484aa5cb0a9dc76f988da983e5152a831c66db00327c8bf597fc7c6e00bf3d5a7914706ca63511429296727b70a852e1b21384d2c6dfc53380d13650a7354766a0abb81c2c92e92722c85a2bfe8a1a81a664bc24b8b70c76c51a3d192e819d6990624f40e3585106aa07019a4c1161e376c082748774c34b0bcb5391c0cb34ed8aa4a5b9cca4f682e6ff3748f82ee78a5636f84c878148cc7020890befffaa4506cebbef9a3f7c67178f2",k,64);
  if(ac==4&&!strcmp(av[1],"-m")){
    addr=value(av[2]);
    n=value(av[3]);
    if(addr<0||n<0||n>FILEMAX)return 2;
    mem=(char *)addr;
    while(j<n){
      b[j]=mem[j];
      j++;
    }
    digest(b,n);
    out(1,"  memory ");
    dec(n);
    putchar(10);
    return 0;
  }
  if(ac==3&&!strcmp(av[1],"-z")){
    int slot=find(av[2]);
    if(!slot)return 1;
    n=lzdecode(bytes(slot),length(slot),b,FILEMAX);
    if(n<0)return 2;
    return inventory(b,n);
  }
  if(ac==3&&!strcmp(av[1],"-a")){
    f=open(av[2],0);
    if(f<0)return 1;
    n=read(f,b,FILEMAX);
    close(f);
    return inventory(b,n);
  }
  if(ac<2){
    out(2,"usage: sha FILE...\n");
    return 2;
  }
  while(i<ac){
    f=open(av[i],0);
    if(f<0){
      weprintf("open %s:",av[i]);
      return 1;
    }
    n=read(f,b,FILEMAX);
    close(f);
    if(n<0)return 1;
    digest(b,n);
    out(1,"  ");
    out(1,av[i]);
    putchar(32);
    dec(n);
    putchar(10);
    i++;
  }
  return 0;
}

