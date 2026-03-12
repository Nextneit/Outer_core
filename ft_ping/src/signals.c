#include "../include/ft_ping.h"

static t_ping_config	*g_config = NULL;

static void	handle_sigint(int sig){
	(void)sig;
	print_statistics(g_config);
	close(g_config->sockfd);
	free(g_config);
	exit(0);
}

void	setup_signal_handlers(t_ping_config *config){
	g_config = config;
	signal(SIGINT, handle_sigint);
}
