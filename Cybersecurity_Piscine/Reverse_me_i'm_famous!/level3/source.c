#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void	___syscall_malloc(void)
{
	puts("Nope.");
	exit(1);
}

void	____syscall_malloc(void)
{
	puts("Good job.");
}

int		main(void)
{
	char	input[36];
	char	buffer[9];
	char	tmp[4];
	int		result;
	int		j;
	long	i;

	printf("Please enter key: ");
	if (scanf("%35s", input) != 1)
		___syscall_malloc();

	if (input[0] != '4' || input[1] != '2')
		___syscall_malloc();

	memset(buffer, 0, 9);
	buffer[0] = '*';
	tmp[3] = '\0';

	i = 2;
	j = 1;
	while (strlen(buffer) < 8)
	{
		tmp[0] = input[i];
		tmp[1] = input[i + 1];
		tmp[2] = input[i + 2];
		buffer[j] = (char)atoi(tmp);
		i += 3;
		j += 1;
	}
	buffer[j] = '\0';

	result = strcmp(buffer, "********");
	switch (result)
	{
		case -2:	___syscall_malloc(); break;
		case -1:	___syscall_malloc(); break;
		case  0:	____syscall_malloc(); break;
		case  1:	___syscall_malloc(); break;
		case  2:	___syscall_malloc(); break;
		case  3:	___syscall_malloc(); break;
		case  4:	___syscall_malloc(); break;
		case  5:	___syscall_malloc(); break;
		case  115:	___syscall_malloc(); break;
		default:	___syscall_malloc(); break;
	}
	return (0);
}