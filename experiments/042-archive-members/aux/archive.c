#include "runtime"
int main(int ac,char **av){


      char *p=(char *)INPUT;


      char *q=(char *)TRANSFER;


      char *test=(char *)LOADBUF;


      char *s=0;


      int i=2;


      int j=0;


      int k=0;


      int n=0;


      int z=0;


      int at=0;


      int hi=0;


      int lo=0;


      if(ac<3)return 2;


      while(i<ac){


            k=find(av[i]);


            if(!k)return 1;


            n=length(k);


            z=flen(av[i]);


            if(n>65534+1||z>NAMEMAX||at+3+z+n+1>FILEMAX)return 3;


            p[at]=z;


            lo=n;


            hi=0;


            while(lo>255){


                  lo=lo-256;


                  hi++;


            }


            p[at+1]=lo;


            p[at+2]=hi;


            at=at+3;


            j=0;


            while(j<z){


                  p[at]=av[i][j];


                  at++;


                  j++;


            }


            j=0;


            s=bytes(k);


            while(j<n){


                  p[at]=s[j];


                  at++;


                  j++;


            }


            i++;


      }


      p[at]=0;


      at++;


      n=lzencode(p,at,q,FILEMAX);


      if(n<0||n>32768)return 4;


      if(fsput(av[1],q,n))return 5;


      k=find(av[1]);


      n=lzdecode(bytes(k),length(k),test,FILEMAX);


      if(n!=at||!equal(p,test,at))return 6;


      return 0;


}



