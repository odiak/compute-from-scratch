#include "libc"
#include "fs42"
int ccaddr=0;
int have=0;
int csize=0;

int number(int n){
  int q=0;
  if(n<0){
    fdch(1,45);
    n=0-n;
  }
  while(n>9){
    n=n-10;
    q++;
  }
  if(q)number(q);
  fdch(1,n+48);
  return 0;
}

int getline(char *p,int cap){
  int n=0;
  int bad=0;
  char c=0;
  while(1){
    if(read(0,(char *)(EDITBUF+FILEMAX+4096),1)<1)return -1;
    c=((char *)(EDITBUF+FILEMAX+4096))[0];
    if(c==13)c=10;
    if(c==10){
      fdch(1,10);
      break;
    }
    if(c==8||c==127){
      if(n){
        n--;
        out(1,"\b \b");
      }
    }
    else{
      fdch(1,c);
      if(!c)bad=1;
      if(n<cap-1){
        p[n]=c;
        n++;
      }
      else bad=1;
    }
  }
  p[n]=0;
  if(bad)return -1;
  return n;
}

int words(char *s,char **v){
  int i=0;
  int j=0;
  int n=0;
  int q=0;
  while(s[i]){
    while(s[i]&&s[i]<33)i++;
    if(!s[i])break;
    if(n==64)return -1;
    v[n]=s+j;
    n++;
    q=0;
    while(s[i]){
      if(!q&&s[i]<33)break;
      if(s[i]==34||s[i]==39){
        if(!q)q=s[i];
        else if(q==s[i])q=0;
        else{
          s[j]=s[i];
          j++;
        }
        i++;
      }
      else{
        s[j]=s[i];
        i++;
        j++;
      }
    }
    if(q)return -1;
    if(s[i])i++;
    s[j]=0;
    j++;
  }
  v[n]=(char *)0;
  return n;
}

int audit(int count){
  char *old=(char *)SNAPSHOT;
  char *d=0;
  char *s=0;
  char *p=(char *)(TRANSFER+FILEMAX+16);
  int i=0;
  int j=0;
  int k=0;
  int n=0;
  if(fscheck())return 1;
  while(i<count){
    d=old+1024+i*128;
    if(d[0]){
      j=0;
      while(j<d[0]){
        p[j]=d[j+4];
        j++;
      }
      p[j]=0;
      k=find(p);
      n=d[2]+d[3]*256;
      if(!k||length(k)!=n)return 2;
      if(!equal(bytes(k),old+5120+i*32768,n)){
        out(1,"mismatch ");
        puts(p);
        return 3;
      }
    }
    i++;
  }
  puts("all snapshot files byte-equal");
  return 0;
}

int importold(void){
  char *base=(char *)DISK;
  char *old=(char *)SNAPSHOT;
  char *d=0;
  char *p=(char *)(TRANSFER+FILEMAX+16);
  char *image=(char *)IMAGE;
  int *h=(int *)IMAGE;
  int i=0;
  int j=0;
  int n=0;
  while(i<16*256*256){
    old[i]=base[i];
    i++;
  }
  if(!equal(old+1024,base+1024,16*256*256-1024))return 1;
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
  if(fsput("_legacy",old,5120))return 2;
  i=0;
  while(i<24){
    d=old+1024+i*128;
    if(d[0]){
      j=0;
      while(j<d[0]){
        p[j]=d[j+4];
        j++;
      }
      p[j]=0;
      n=d[2]+d[3]*256;
      if(fsput(p,old+5120+i*32768,n))return 3;
      if(audit(i+1))return 4;
    }
    i++;
  }
  return audit(24);
}

int publish(void){
  char *d=(char *)(DISK+1024);
  char *s=0;
  char *t=(char *)(DISK+5120);
  int k=find("start");
  int i=0;
  int n=0;
  if(!k||length(k)>32768||audit(24))return 1;
  n=length(k);
  s=bytes(k);
  while(i<128){
    d[i]=0;
    i++;
  }
  d[0]=5;
  d[2]=n;
  d[3]=0;
  while(n>255){
    d[3]++;
    n=n-256;
  }
  d[2]=n;
  d[80]=165;
  s="start";
  i=0;
  while(i<5){
    d[i+4]=s[i];
    i++;
  }
  s=bytes(k);
  i=0;
  while(i<length(k)){
    t[i]=s[i];
    i++;
  }
  if(!equal(t,s,length(k)))return 2;
  return fscommit();
}

int make(char *name,int dest){
  int k=find(name);
  int n=0;
  int i=0;
  char *src=(char *)INPUT;
  char *p=(char *)OUTPUT;
  char *d=(char *)dest;
  char *s=0;
  if(dest!=USER&&dest!=APP)return 0;
  if(!k||length(k)>SOURCEMAX)return 0;
  s=bytes(k);
  while(i<length(k)){
    src[i]=s[i];
    i++;
  }
  n=invoke(ccaddr,(int)src,length(k),OUTPUT);
  if(n<4||n>CODEMAX||align4(n)!=n)return 0;
  i=0;
  while(i<n){
    d[i]=p[i];
    i++;
  }
  return n;
}

int replacefile(char *name,char *from,char *to){
  int k=find(name);
  char *s=0;
  char *d=(char *)INPUT;
  int n=0;
  int i=0;
  int j=0;
  int at=0;
  int a=flen(from);
  int b=flen(to);
  if(!k||!a)return 1;
  s=bytes(k);
  n=length(k);
  while(i<n){
    if(i+a<n+1&&equal(s+i,from,a)){
      if(at+b>FILEMAX)return 2;
      j=0;
      while(j<b){
        d[at]=to[j];
        at++;
        j++;
      }
      i=i+a;
    }
    else{
      if(at==FILEMAX)return 2;
      d[at]=s[i];
      at++;
      i++;
    }
  }
  return fsput(name,d,at);
}

int decimal(char *s){
  int n=0;
  while(*s>47&&*s<58){
    if(n>FILEMAX)return -1;
    n=n*10+*s-48;
    s++;
  }
  return n;
}

int editfile(char *name){
  char *b=(char *)EDITBUF;
  char *l=b+FILEMAX+8192;
  char *p=0;
  int n=0;
  int k=find(name);
  int i=0;
  int j=0;
  int a=0;
  int z=0;
  int t=0;
  int ln=0;
  if(k){
    n=length(k);
    p=bytes(k);
    while(i<n){
      b[i]=p[i];
      i++;
    }
  }
  puts("edit: p; i/r/d N text; w save; q discard");
  while(1){
    out(1,"edit42> ");
    if(getline(l,4096)<0)continue;
    if(!strcmp(l,"q"))return 0;
    if(!strcmp(l,"w")){
      if(fsput(name,b,n))puts("save failed");
      else puts("saved in working image");
      continue;
    }
    if(l[0]==112){
      write(1,b,n);
      fdch(1,10);
      continue;
    }
    i=1;
    while(l[i]==32)i++;
    ln=decimal(l+i);
    while(l[i]>47&&l[i]<58)i++;
    a=0;
    j=1;
    while(a<n&&j<ln){
      if(b[a]==10)j++;
      a++;
    }
    if(ln<1||j!=ln){
      puts("line error");
      continue;
    }
    z=a;
    t=0;
    if(l[0]==114||l[0]==100){
      if(a==n){
        puts("no line");
        continue;
      }
      while(z<n&&b[z]!=10)z++;
      if(z<n)z++;
    }

    if(l[0]!=105&&l[0]!=114&&l[0]!=100){
      puts("edit error");
      continue;
    }
    if(l[0]!=100){
      if(l[i]!=32){
        puts("missing text");
        continue;
      }
      i++;
      t=flen(l+i)+1;
    }
    if(n+t-(z-a)>FILEMAX){
      puts("capacity");
      continue;
    }
    if(t>z-a){
      j=n;
      while(j>z){
        j--;
        b[j+t-(z-a)]=b[j];
      }
    }
    else{
      j=z;
      while(j<n){
        b[j+t-(z-a)]=b[j];
        j++;
      }
    }
    n=n+t-(z-a);
    if(t){
      j=0;
      while(j<t-1){
        b[a+j]=l[i+j];
        j++;
      }
      b[a+j]=10;
    }
  }
  return 0;
}

int extractnew(char *file,char *member){
  int k=find(file);
  char *p=0;
  int n=0;
  int i=0;
  int z=0;
  int len=0;
  int at=0;
  int size=0;
  int found=0;
  if(!k)return 1;
  p=bytes(k);
  n=length(k);
  while(i<n&&p[i]){
    z=p[i];
    if(z>NAMEMAX||i+3+z>n)return 2;
    len=p[i+1]+p[i+2]*256;
    if(i+3+z+len>n)return 2;
    if(flen(member)==z&&equal(member,p+i+3,z)){
      if(found)return 2;
      found=1;
      at=i+3+z;
      size=len;
    }
    i=i+3+z+len;
  }
  if(i!=n-1||!found||p[i])return 2;
  return fsput(member,p+at,size);
}

int main(int ac,char **av){
  char *l=(char *)(EDITBUF+FILEMAX+16384);
  char **v=(char **)(EDITBUF+FILEMAX+24576);
  char *p=0;
  char *q=0;
  int n=0;
  int k=0;
  int r=0;
  int i=0;
  int *d=0;
  ccaddr=COMPILER;
  if(ac>1&&!strcmp(av[1],"init")){
    r=importold();
    number(r);
    fdch(1,10);
    if(r)return r;
  }
  if(fscheck())return 3;
  puts("042 staging console (no automatic disk writes)");
  while(1){
    out(1,"stage> ");
    if(getline(l,4096)<0)continue;
    ac=words(l,v);
    if(ac<1)continue;
    r=0;
    if(!strcmp(v[0],"quit"))return 0;
    else if(!strcmp(v[0],"audit"))r=audit(24);
    else if(!strcmp(v[0],"check"))r=fscheck();
    else if(!strcmp(v[0],"publish"))r=publish();
    else if(!strcmp(v[0],"commit"))r=fscommit();
    else if(!strcmp(v[0],"list")){
      k=1;
      while(k<FILES+1){
        d=node(k);
        if(d[0]){
          write(1,(char *)(d+4),d[0]);
          fdch(1,32);
          number(d[1]);
          fdch(1,10);
        }
        k++;
      }
    }

    else if(!strcmp(v[0],"show")&&ac==2){
      k=find(v[1]);
      if(!k)r=1;
      else write(1,bytes(k),length(k));
    }
    else if(!strcmp(v[0],"edit")&&ac==2)r=editfile(v[1]);
    else if(!strcmp(v[0],"replace")&&ac==4)r=replacefile(v[1],v[2],v[3]);
    else if(!strcmp(v[0],"copy")&&ac==3){
      k=find(v[1]);
      if(!k)r=1;
      else r=fsput(v[2],bytes(k),length(k));
    }
    else if(!strcmp(v[0],"extract")&&ac==3)r=extractnew(v[1],v[2]);
    else if(!strcmp(v[0],"put")&&ac==3)r=fsput(v[1],v[2],flen(v[2]));
    else if(!strcmp(v[0],"remove")&&ac==2)r=erasefile(v[1]);
    else if(!strcmp(v[0],"build")&&ac==2){
      n=make(v[1],USER);
      if(n){
        have=n;
        number(n);
        fdch(1,10);
      }
      else r=1;
    }

    else if(!strcmp(v[0],"save")&&ac==2){
      if(!have)r=1;
      else r=fsnative(v[1],USER,have);
    }
    else if(!strcmp(v[0],"load")&&ac==2){
      n=native(v[1],USER);
      if(n)have=n;
      else r=1;
    }
    else if(!strcmp(v[0],"run")&&ac>1){
      if(!have)r=1;
      else r=invoke(USER,ac-1,(int)(v+1),0);
    }
    else if(!strcmp(v[0],"install")&&have){
      p=(char *)USER;
      q=(char *)COMPILER;
      i=0;
      while(i<have){
        q[i]=p[i];
        i++;
      }
      csize=have;
      ccaddr=COMPILER;
    }
    else if(!strcmp(v[0],"compare")&&have){
      p=(char *)USER;
      q=(char *)COMPILER;
      if(csize!=have)r=1;
      else if(!equal(p,q,have))r=1;
    }
    else if(!strcmp(v[0],"size")){
      number(have);
      fdch(1,10);
    }
    else r=2;
    if(r){
      out(1,"status ");
      number(r);
      fdch(1,10);
    }
  }
  return 0;
}

