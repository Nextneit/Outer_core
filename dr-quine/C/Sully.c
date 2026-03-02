#include<stdio.h>
#include<stdlib.h>

int main(){
	int i=5;
	char*s="#include<stdio.h>%1$c#include<stdlib.h>%1$c%1$cint main(){%1$c%2$cint i=%3$d;%1$c%2$cchar*s=%4$c%5$s%4$c;%1$c%2$cchar f[32],c[128];%1$c%1$c%2$cif(i<0)%1$c%2$c%2$creturn 0;%1$c%2$csprintf(f,%4$cSully_%%d.c%4$c,i);%1$c%2$cFILE*fp=fopen(f,%4$cw%4$c);%1$c%2$cfprintf(fp,s,10,9,i-1,34,s);%1$c%2$cfclose(fp);%1$c%2$cif(i>0){%1$c%2$c%2$csprintf(c,%4$cgcc -Wall -Wextra -Werror Sully_%%d.c -o Sully_%%d && ./Sully_%%d%4$c,i,i,i);%1$c%2$c%2$csystem(c);%1$c%2$c}%1$c%2$creturn 0;%1$c}%1$c";
	char f[32],c[128];

	if(i<0)
		return 0;
	sprintf(f,"Sully_%d.c",i);
	FILE*fp=fopen(f,"w");
	fprintf(fp,s,10,9,i-1,34,s);
	fclose(fp);
	if(i>0){
		sprintf(c,"gcc -Wall -Wextra -Werror Sully_%d.c -o Sully_%d && ./Sully_%d",i,i,i);
		system(c);
	}
	return 0;
}
