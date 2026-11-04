int puts(char *s){int i=0;while(s[i]){putchar(s[i]);i=i+1;}putchar('\n');return i+1;}int strcmp(char *a,char *b){int i=0;while(a[i]){if(a[i]-b[i]){return a[i]-b[i];}i=i+1;}return a[i]-b[i];}
