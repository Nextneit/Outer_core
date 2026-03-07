#include "../include/ft_ping.h"

void	print_help(void)
{
    printf("Usage: ft_ping [OPTION...] HOST\n");
    printf("Send ICMP ECHO_REQUEST packets to network hosts.\n\n");
    printf("Options:\n");
    printf("  -v              verbose output\n");
    printf("  -?              give this help list\n\n");
    printf("Report bugs to <your_email@example.com>.\n");
}

static int	parse_options(int argc, char **argv, t_ping_config *config, int *target){
	int	i;

	i = 1;
	config->verbose = false;
	*target = -1;
	while (i < argc){
		if (argv[i][0] == '-'){
			if (strncmp(argv[i], "-v", strlen(argv[i])) == 0)
				config->verbose = true;
			else if (strncmp(argv[i], "-?", strlen(argv[i])) == 0
				|| strncmp(argv[i], "--help", strlen(argv[i])) == 0){
				print_help();
				exit(0);
			}
			else
				return (printf("ft_ping: invalid option '%s'\n", argv[i]), 1);
		}
		else{
			if (*target != -1)
				return (printf("ft_ping: too many arguments\n"), 1);
			*target = i;
		}
		i++;
	}
	return (0);
}

int	parse_arguments(int argc, char **argv, t_ping_config *config){
	int	*target;
	
	target = 0;
	if (argc < 2)
		return (printf("Error: missing host operand\n"), 1);
	if (parse_options(argc, argv, config, target) == 1)
		return (1);
	return (0);
}
