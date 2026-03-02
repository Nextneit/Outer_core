/*Comment*/
#include<stdio.h>

#define S "/*Comment*/%1$c#include<stdio.h>%1$c%1$c#define S %2$c%3$s%2$c%1$c#define F {FILE*f=fopen(%2$cGrace_kid.c%2$c,%2$cw%2$c);fprintf(f,S,10,34,S);fclose(f);}%1$c#define M int main(){F return 0;}%1$cM%1$c"
#define F {FILE*f=fopen("Grace_kid.c","w");fprintf(f,S,10,34,S);fclose(f);}
#define M int main(){F return 0;}
M
