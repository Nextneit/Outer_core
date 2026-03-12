#include "../include/ft_ping.h"

int	main(int argc, char **argv){
	t_ping_config *config;
	struct	timeval	send_time;

	config = calloc(1, sizeof(t_ping_config));
	if (!config)
		return (perror("ft_ping: malloc"), 1);
	if (parse_arguments(argc, argv, config) == 1)
		return (free(config), 1);
	if (resolve_hostname(config->target, config->resolved_ip) == 1)
		return (free(config), 1);
	config->sockfd = create_raw_socket(config);
	if (config->sockfd < 0)
		return (free(config), 1);
	config->sequence = 1;
	printf("PING %s (%s): %d data bytes\n", config->target, config->resolved_ip, config->packet_size);
	setup_signal_handlers(config);
	gettimeofday(&config->start_time, NULL);
	while (1){
		gettimeofday(&send_time, NULL);
        if (config->deadline > 0 && (send_time.tv_sec - config->start_time.tv_sec) >= config->deadline)
            break;
		if (send_ping(config) != 0)
        	break;
		receive_ping(config, &send_time);
		sleep(1);
	}
	return (0);
}
