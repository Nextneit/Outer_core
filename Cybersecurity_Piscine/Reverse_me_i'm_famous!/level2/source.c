#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void	no(void)
{
	puts("Nope.");
	exit(1);
}

void	ok(void)
{
	puts("Good job.");
}

int	main(void)
{
	char	input[36];
	char	buffer[9];
	char	tmp[4];
	int		i;
	int		j;

	printf("Please enter key: ");
	if (scanf("%35s", input) != 1)
		no();

	if (input[0] != '0' || input[1] != '0')
		no();

	memset(buffer, 0, 9);
	buffer[0] = 'd';
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

	if (strcmp(buffer, "delabere") != 0)
		no();
	ok();
	return (0);
}