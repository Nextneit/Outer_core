/*
	Outer comment
*/

#include <stdio.h>

void ft(){
	// Inner comment in function
	char*s="/*%1$c%2$cOuter comment%1$c*/%1$c%1$c#include <stdio.h>%1$c%1$cvoid ft(){%1$c%2$c// Inner comment in function%1$c%2$cchar*s=%3$c%4$s%3$c;%1$c%2$cprintf(s,10,9,34,s);%1$c}%1$c%1$cint main(){%1$c%2$c/* Inner comment in main */%1$c%2$cft();%1$c%2$creturn 0;%1$c}%1$c";
	printf(s,10,9,34,s);
}

int main(){
	/* Inner comment in main */
	ft();
	return 0;
}
