#include "runtime"
int value(char *s){
  int n=0;
  while(*s>47&&*s<58){
    n=n*10+*s-48;
    s++;
  }
  return n;
}

int main(int ac,char **av){
  int n=0;
  int i=0;
  int f=0;
  if(ac!=3)return 2;
  n=value(av[2]);
  if(n<1||n>3000)return 2;
  f=open(av[1],577);
  if(f<0)return 1;
  out(f,"#include \"runtime\"\nint number(int n){int q=0;while(n>9){n=n-10;q++;}if(q)number(q);putchar(n+48);return 0;}\nint main(void){int accumulator_total=0;\n");
  while(i<n){
    if(out(f,"  accumulator_total++;\n"))return 1;
    i++;
  }
  out(f,"out(1,\"red count \");number(accumulator_total);putchar(10);return 0;}\n");
  return close(f);
}

