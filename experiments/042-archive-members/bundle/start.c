#include "fs42"
int main(int ac,char **av){
  int r=fsmount();
  if(r){
    uartput(70);
    uartput(48+r);
    uartput(10);
    return r;
  }
  if(!native("cc",COMPILER)||!native("dev",SHELL))return 2;
  return invoke(SHELL,ac,(int)av,0);
}

