#include "../include/ft_ping.h"

int	main(int argc, char **argv){
	t_ping_config *config;

	config = malloc(sizeof(t_ping_config));
	if (!config)
		return (perror("ft_ping: malloc"), 1);
	if (parse_arguments(argc, argv, config) == 1)
		return (free(config), 1);
	return (0);
}