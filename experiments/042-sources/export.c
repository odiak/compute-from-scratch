#include "runtime"
int main(int ac,char **av){


      char *image=(char *)SNAPSHOT;


      char *base=(char *)DISK;


      char *list=0;


      char *name=(char *)(TRANSFER+FILEMAX+32);


      char *d=0;


      char *p=0;


      int k=0;


      int n=0;


      int i=0;


      int j=0;


      int at=0;


      int count=0;


      int len=0;


      if(ac!=3||strcmp(av[2],"yes"))return 2;


      k=find(av[1]);


      if(!k)return 1;


      list=bytes(k);


      len=length(k);


      while(i<16*256*256){


            image[i]=0;


            i++;


      }


      while(at<len){


            j=0;


            while(at<len&&list[at]!=10){


                  if(j==12||!(list[at]>47&&list[at]<58||list[at]>64&&list[at]<91||list[at]>96&&list[at]<123))return 3;


                  name[j]=list[at];


                  j++;


                  at++;


            }


            at++;


            if(!j)continue;


            name[j]=0;


            if(count==24)return 3;


            k=find(name);


            if(!k||length(k)>32768)return 4;


            n=length(k);


            d=image+1024+count*128;


            d[0]=j;


            d[2]=n;


            d[3]=0;


            while(n>255){


                  d[3]++;


                  n=n-256;


            }


            d[2]=n;


            d[80]=165;


            i=0;


            while(i<j){


                  d[i+4]=name[i];


                  i++;


            }


            n=length(k);


            p=bytes(k);


            i=0;


            while(i<n){


                  image[5120+count*32768+i]=p[i];


                  i++;


            }


            if(!equal(image+5120+count*32768,p,n))return 5;


            count++;


      }


      set32(image+LEGACY_MARKER,LEGACY_CAP);
  i=1024;


      while(i<16*256*256){


            base[i]=image[i];


            i++;


      }


      if(!equal(base+1024,image+1024,16*256*256-1024))return 6;


      if(diskcommit())return 7;


      puts("SOURCE-ONLY DISK WRITTEN. Stop/reboot; batch bootplan. No return into mounted environment.");


      while(1){


      }


      return 0;


}



