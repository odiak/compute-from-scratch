#include "shellcore"
#include "process"
int planat=0;
int planend=0;

int startplan(char *name){
  int k=find(name);
  int i=0;
  char *p=0;
  char *q=(char *)PLANBUF;
  if(planend||!k||length(k)>FILEMAX)return 1;
  p=bytes(k);
  while(i<length(k)){
    q[i]=p[i];
    i++;
  }
  planat=0;
  planend=i;
  return 0;
}

int command(int ac,char **v){
  int n=0;
  int k=0;
  int i=0;
  int r=0;
  int *d=0;
  char *p=0;
  char *q=0;
  if(!strcmp(v[0],"quit")&&ac==1)return -2;
  if(!strcmp(v[0],"plan")&&ac==2)return startplan(v[1]);
  if(!strcmp(v[0],"list")){
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
    return 0;
  }
  if(!strcmp(v[0],"show")&&ac==2){
    k=find(v[1]);
    if(!k)return 1;
    return write(1,bytes(k),length(k))<0;
  }
  if(!strcmp(v[0],"check"))return fscheck();
  if(!strcmp(v[0],"edit")&&ac==2)return editfile(v[1]);
  if(!strcmp(v[0],"build")&&ac==2){
    n=make(v[1],USER);
    if(!n)return 1;
    have=n;
    number(n);
    fdch(1,10);
    return 0;
  }
  if(!strcmp(v[0],"load")&&ac==2){
    n=native(v[1],USER);
    if(!n)return 1;
    have=n;
    return 0;
  }
  if(!strcmp(v[0],"compare")){
    if(!have||have!=csize)return 1;
    return !equal((char *)USER,(char *)COMPILER,have);
  }
  if(!strcmp(v[0],"install")){
    if(!have)return 1;
    i=0;
    p=(char *)USER;
    q=(char *)COMPILER;
    while(i<have){
      q[i]=p[i];
      i++;
    }
    csize=have;
    return 0;
  }
  if(!strcmp(v[0],"save")&&ac==2){
    if(!have)return 1;
    r=fsnative(v[1],USER,have);
  }
  else if(!strcmp(v[0],"copy")&&ac==3){
    k=find(v[1]);
    if(!k)return 1;
    r=fsput(v[2],bytes(k),length(k));
  }
  else if(!strcmp(v[0],"replace")&&ac==4)r=replacefile(v[1],v[2],v[3]);
  else if(!strcmp(v[0],"put")&&ac==3)r=fsput(v[1],v[2],strlen(v[2]));
  else if(!strcmp(v[0],"extract")&&ac==3)r=extractnew(v[1],v[2]);
  else if(!strcmp(v[0],"remove")&&ac==2)r=erasefile(v[1]);
  else return pipeline(ac,v);
  if(!r)r=fscommit();
  return r;
}

int main(int ac,char **av){
  char *l=(char *)(EDITBUF+FILEMAX+16384);
  char **v=(char **)(EDITBUF+FILEMAX+24576);
  char *p=(char *)PLANBUF;
  int n=0;
  int r=0;
  int planned=0;
  ccaddr=COMPILER;
  csize=codesize("cc");
  if(ac>1&&startplan(av[1]))return 2;
  puts("042 development console");
  while(1){
    planned=planend>0;
    if(planned){
      n=0;
      while(planat<planend&&p[planat]!=10){
        if(n==4095){
          planend=0;
          break;
        }
        l[n]=p[planat];
        n++;
        planat++;
      }
      planat++;
      l[n]=0;
      out(1,"+ ");
      puts(l);
      if(planat>planend-1)planend=0;
    }
    else{
      out(1,"dev42> ");
      if(getline(l,4096)<0)continue;
    }
    ac=words(l,v);
    if(ac<1)continue;
    r=command(ac,v);
    if(r==-2)return 0;
    if(r){
      out(1,"status ");
      number(r);
      fdch(1,10);
      if(planned){
        planend=0;
        puts("plan stopped");
      }
    }
  }
  return 0;
}

