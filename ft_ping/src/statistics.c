#include "../include/ft_ping.h"

void    print_statistics(t_ping_config *config){
	struct timeval	end_time;
	long			elapsed_ms;
	double			avg_rtt;
	double			mdev_rtt;
	int				loss_pct;

	gettimeofday(&end_time, NULL);
	elapsed_ms = (end_time.tv_sec - config->start_time.tv_sec) * 1000
           + (end_time.tv_usec - config->start_time.tv_usec) / 1000;
	
	printf("\n--- %s ping statistics ---\n", config->target);

	loss_pct = 0;

	if (config->stats.packets_sent > 0)
		loss_pct = (int)(100 - (config->stats.packets_received * 100.0
					/ config->stats.packets_sent));
	
	printf("%lu packets transmitted, %lu received, %d%% packet loss, time %ldms\n",
				config->stats.packets_sent,
				config->stats.packets_received,
				loss_pct,
				elapsed_ms);
	if (config->stats.packets_received > 0){
        avg_rtt = config->stats.sum_rtt / config->stats.packets_received;
        mdev_rtt = sqrt(config->stats.sum_sq_rtt / config->stats.packets_received
                    - avg_rtt * avg_rtt);
        printf("rtt min/avg/max/mdev = %.3f/%.3f/%.3f/%.3f ms\n",
               config->stats.min_rtt, avg_rtt,
               config->stats.max_rtt, mdev_rtt);
	}
}
