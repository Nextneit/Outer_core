#include "../include/ft_ping.h"

int	main(int argc, char **argv){
	t_ping_config *config;
	struct	timeval	send_time;

	config = malloc(sizeof(t_ping_config));
	if (!config)
		return (perror("ft_ping: malloc"), 1);
	if (parse_arguments(argc, argv, config) == 1)
		return (free(config), 1);
	if (resolve_hostname(config->target, config->resolved_ip) == 1)
		return (free(config), 1);
	config->sockfd = create_raw_socket();
	if (config->sockfd < 0)
		return (free(config), 1);
	//printf("PING %s (%s): %d data bytes\n", config->target, config->resolved_ip, PACKET_SIZE - 8);
	while (1){
		gettimeofday(&send_time, NULL);
		if (send_ping(config) != 0)
			break;
		receive_ping(config, &send_time);
		sleep(1);
	}
	close(config->sockfd);
	free(config);
	return (0);
}