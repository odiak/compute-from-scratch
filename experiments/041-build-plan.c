int plan(char *name){char *s=(char *)(16656*256*256);char *l=s+256*256;char **v=(char **)(16688*256*256);char *d=(char *)(16405*256*256);char *p=(char *)(16576*256*256);int f=0;int n=0;int at=0;int k=0;int ac=0;int have=0;int r=0;int i=0;int row=0;reset();f=open(name,0);if(f<0){weprintf("plan open %s:",name);return 1;}n=read(f,s,32768);r=close(f);if(n<0||r<0)return 1;while(at<n){k=0;row++;while(at<n&&s[at]!=10){if(!s[at]||k>4094){puts("plan: invalid/overlong line");return 2;}l[k]=s[at];k++;at++;}at++;l[k]=0;if(!k||l[0]==35)continue;ac=tokens(l,v);if(ac<0)return 2;if(!ac)continue;r=2;out(1,"plan line ");number(row);fdch(1,10);
if(!strcmp(v[0],"merge")&&ac==4)r=merge(v[1],v[2],v[3]);else if(!strcmp(v[0],"clean")&&ac==2)r=clean(v[1]);else if(!strcmp(v[0],"erase")&&ac==2)r=erase(v[1]);else if(!strcmp(v[0],"archive")&&ac>2)r=archive(ac-1,v+1);else if(!strcmp(v[0],"extract")&&ac==3)r=extract(v[1],v[2]);else if(!strcmp(v[0],"build")&&ac==2){k=make(v[1],16576*256*256);r=!k;if(k)have=k;}
else if(!strcmp(v[0],"install")&&ac==1){if(have)r=putcompiler(have);}
else if(!strcmp(v[0],"compare")&&ac==1){if(have)r=eqcompiler(have);}
else if(!strcmp(v[0],"save")&&ac==3){r=blobsave(v[1],v[2],have);}
else if(!strcmp(v[0],"load")&&ac==3){k=blobload(v[1],v[2]);r=!k;if(k)have=k;}
else if(!strcmp(v[0],"exec")&&ac>1){if(have)r=execute(16576*256*256,ac-1,v+1);}
else if(!strcmp(v[0],"source")&&ac>1)r=pipeline(ac-1,v+1);
else if(!strcmp(v[0],"remove")&&ac==2){k=lookup(v[1]);if(k){char *e=(char *)(16448*256*256+1024);e=e+(k-1)*128;e[0]=0;r=diskcommit();}else r=1;}
if(r){out(1,"plan stopped at line ");number(row);fdch(1,10);return r;}}puts("plan complete");return 0;}
