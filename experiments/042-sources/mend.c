#include "runtime"
int locate(char *s,int n,char *pat,int at){

    int k=flen(pat);

    while(at+k<n+1){

        if(equal(s+at,pat,k))return at;

        at++;

    }

    return -1;

}


int dec(int n){

    int q=0;

    while(n>9){

        n=n-10;

        q++;

    }

    if(q)dec(q);

    fdch(1,n+48);

    return 0;

}


int main(int ac,char **av){

    char *p=0;

    char *q=0;

    char *t=(char *)INPUT;

    int k=0;

    int n=0;

    int a=0;

    int b=0;

    int i=0;

    int j=0;

    int at=0;

    int z=0;

    if(ac==6&&!strcmp(av[1],"cut")){

        k=find(av[2]);

        if(!k)return 1;

        p=bytes(k);

        n=length(k);

        a=locate(p,n,av[3],0);

        if(a<0)return 2;

        b=locate(p,n,av[4],a);

        if(b<0)return 2;

        k=find(av[5]);

        if(!k)return 1;

        q=bytes(k);

        z=length(k);

        if(a+z+n-b>FILEMAX)return 3;

        while(i<a){

            t[at]=p[i];

            at++;

            i++;

        }

        i=0;

        while(i<z){

            t[at]=q[i];

            at++;

            i++;

        }

        i=b;

        while(i<n){

            t[at]=p[i];

            at++;

            i++;

        }

        return fsput(av[2],t,at);

    }


    if(ac==5&&!strcmp(av[1],"join")){

        k=find(av[3]);

        if(!k)return 1;

        p=bytes(k);

        n=length(k);

        while(i<n){

            t[at]=p[i];

            i++;

            at++;

        }

        k=find(av[4]);

        if(!k||at+length(k)>FILEMAX)return 1;

        p=bytes(k);

        n=length(k);

        i=0;

        while(i<n){

            t[at]=p[i];

            at++;

            i++;

        }

        return fsput(av[2],t,at);

    }


    if(ac==3&&!strcmp(av[1],"list")){

        k=find(av[2]);

        if(!k)return 1;

        p=bytes(k);

        n=length(k);

        while(i<n&&p[i]){

            a=p[i];

            if(i+3+a>n)return 2;

            b=p[i+1]+p[i+2]*256;

            if(i+3+a+b>n)return 2;

            write(1,p+i+3,a);

            fdch(1,32);

            dec(b);

            fdch(1,10);

            i=i+3+a+b;

        }

        return i!=n-1;

    }


    if(ac==6&&!strcmp(av[1],"slice")){

        k=find(av[2]);

        if(!k)return 1;

        p=bytes(k);

        n=length(k);

        a=locate(p,n,av[4],0);

        if(a<0)return 2;

        b=n;

        if(flen(av[5]))b=locate(p,n,av[5],a);

        if(b<a)return 2;

        return fsput(av[3],p+a,b-a);

    }


    return 2;

}


