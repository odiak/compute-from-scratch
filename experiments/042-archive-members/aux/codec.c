#include "runtime"
/* Byte LZ stream: u32 original length; literal tag 0..127 + 1 bytes, or tag 128..255 + distance u16. */
int main(int ac,char **av){

    int k=0;

    int n=0;

    int z=0;

    char *p=0;

    char *q=(char *)INPUT;

    if(ac!=4)return 2;

    k=find(av[2]);

    if(!k)return 1;

    p=bytes(k);

    n=length(k);

    if(!strcmp(av[1],"pack")){

        z=lzencode(p,n,q,FILEMAX);

        if(z<0||fsput(av[3],q,z))return 3;

        k=find(av[3]);

        z=lzdecode(bytes(k),length(k),q,FILEMAX);

        k=find(av[2]);

        if(z!=length(k)||!equal(q,bytes(k),z))return 4;

        return 0;

    }

    if(!strcmp(av[1],"unpack")){

        z=lzdecode(p,n,q,FILEMAX);

        if(z<0)return 3;

        return fsput(av[3],q,z);

    }

    return 2;

}


