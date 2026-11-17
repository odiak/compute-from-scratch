#include "runtime"
int add(char *b,int at,char *s){
  int i=0;
  while(s[i]){
    b[at]=s[i];
    at++;
    i++;
  }
  return at;
}

int main(void){
  char *p=(char *)INPUT;
  char *c=(char *)COMPILER;
  char *u=(char *)USER;
  char *save=(char *)TESTBUF;
  int i=0;
  int at=0;
  int end=0;
  int k=0;
  int pad=0;
  int r=0;
  while(i<CODEMAX){
    save[i]=c[i];
    save[CODEMAX+i]=u[i];
    i++;
  }
  at=add(p,0,"int main(void){return 7;}/*");
  i=at;
  while(i<SOURCEMAX-2){
    p[i]=32;
    i++;
  }
  p[i]=42;
  p[i+1]=47;
  k=invoke(COMPILER,INPUT,SOURCEMAX,OUTPUT);
  if(k<4)r=2;
  if(invoke(COMPILER,INPUT,SOURCEMAX+1,OUTPUT))r=3;
  if(invoke(COMPILER,INPUT,SOURCEMAX,USER)||invoke(COMPILER,INPUT,SOURCEMAX,COMPILER))r=4;
  erasefile("source.edge");

  at=add(p,0,"int main(void){int accumulator_total=0;\n");
  i=0;
  while(i<5400){
    at=add(p,at,"accumulator_total++;\n");
    i++;
  }
  end=at;
  at=add(p,at,"return accumulator_total;}");
  k=invoke(COMPILER,INPUT,at,OUTPUT);
  if(k<4||k>CODEMAX)return 5;
  pad=CODEMAX-k;
  at=end;
  while(pad>0){
    at=add(p,at,"0;");
    pad=pad-4;
  }
  end=at;
  at=add(p,at,"return accumulator_total;}");
  k=invoke(COMPILER,INPUT,at,OUTPUT);
  if(k!=CODEMAX)r=6;
  at=add(p,end,"0;return accumulator_total;}");
  if(invoke(COMPILER,INPUT,at,OUTPUT))r=8;
  i=0;
  while(i<CODEMAX){
    if(save[i]!=c[i]||save[CODEMAX+i]!=u[i])r=9;
    i++;
  }
  if(r){
    out(1,"boundary failure ");
    putchar(r+48);
    putchar(10);
  }
  else puts("source, code, overlap and preservation boundaries PASS");
  return r;
}

