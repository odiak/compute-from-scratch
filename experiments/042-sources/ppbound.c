#include "runtime"
int text(char *p,int at,char *s){
  int i=0;
  while(s[i]){
    p[at]=s[i];
    at++;
    i++;
  }
  return at;
}

int main(void){
  char *p=(char *)INPUT;
  char *saved=(char *)TESTBUF;
  int at=0;
  int i=0;
  int n=0;
  int r=0;
  while(i<CODEMAX){
    saved[i]=((char *)COMPILER)[i];
    saved[CODEMAX+i]=((char *)USER)[i];
    i++;
  }
  at=text(p,0,"#define PAD /**/");
  i=0;
  while(i<2000){
    p[at]=32;
    at++;
    i++;
  }
  at=text(p,at,"\nint main(void){return 7;}\n");
  i=0;
  while(i<98){
    at=text(p,at,"PAD\n");
    i++;
  }
  n=invoke(COMPILER,INPUT,at,OUTPUT);
  if(n<4)r=1;
  at=text(p,at,"PAD\n");
  if(invoke(COMPILER,INPUT,at,OUTPUT))r=2;
  i=0;
  while(i<CODEMAX){
    if(saved[i]!=((char *)COMPILER)[i]||saved[CODEMAX+i]!=((char *)USER)[i])r=3;
    i++;
  }
  if(r)puts("PP boundary FAIL");
  else puts("preprocessor expansion boundary and preservation PASS");
  return r;
}

