/* Generic AArch64 32-bit AND/XOR/LSRV/RORV stubs. Source instruction encoding, emitted in the guest; no compiler bytes. */
int bitinit(void){int *p=(int *)(16768*256*256);int r=54879*256*256+960;p[0]=2562*256*256+32;p[1]=r;p[2]=18946*256*256+32;p[3]=r;p[4]=6850*256*256+9248;p[5]=r;p[6]=6850*256*256+11296;p[7]=r;return 0;}
int bit(int op,int a,int b){return invoke(16768*256*256+(op-1)*8,a,b,0);}
int bx(int a,int b){return bit(2,a,b);}
