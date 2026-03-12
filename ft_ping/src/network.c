#include "../include/ft_ping.h"

// config->ttl controla IP_TTL: cuántos saltos puede dar el paquete antes de ser descartado.
// config->timeout_ms controla SO_RCVTIMEO: cuánto espera recvfrom antes de retornar EAGAIN.
int	create_raw_socket(t_ping_config *config){
    int			sockfd;
    struct timeval		timeout;

    sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sockfd < 0){
        if (errno == EPERM)
            printf("ft_ping: socket: Operation not permitted\n");
        else
            perror("ft_ping: socket");
        return (-1);
    }
    if (setsockopt(sockfd, IPPROTO_IP, IP_TTL, &config->ttl, sizeof(config->ttl)) < 0){
        perror("ft_ping: setsockopt TTL");
        close(sockfd);
        return (-1);
    }
    // timeout_ms se divide en segundos + microsegundos para struct timeval
    timeout.tv_sec = config->timeout_ms / 1000;
    timeout.tv_usec = (config->timeout_ms % 1000) * 1000;
    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) < 0){
        perror("ft_ping: setsockopt timeout");
        close(sockfd);
        return (-1);
    }
    return (sockfd);
}

int	send_ping(t_ping_config *config){
    char	packet[config->packet_size + 8];
	struct	sockaddr_in addr;
	int		bytes_sent;

	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	inet_pton(AF_INET, config->resolved_ip, &addr.sin_addr);
	create_icmp_packet(packet, config->sequence, config->packet_size);
	bytes_sent = sendto(config->sockfd, packet, config->packet_size + 8, 0, (struct sockaddr *)&addr, sizeof(addr));
	if (bytes_sent < 0)
		return (perror("ft_ping: sendto"), 1);
	config->stats.packets_sent++;
	config->sequence++;
	return (0);
}

int	receive_ping(t_ping_config *config, struct timeval *send_time){
	char			buffer[1024];
	struct sockaddr_in	addr;
	socklen_t		addr_len;
	struct timeval		recv_time;
	int			bytes_received;
	struct ip		*ip_hdr;
	struct icmp		*icmp_hdr;
	int			ip_hdr_len;
	double			rtt;

	while (1){
		addr_len = sizeof(addr);
		bytes_received = recvfrom(config->sockfd, buffer, sizeof(buffer), 0, (struct sockaddr *)&addr, &addr_len);
		if (bytes_received < 0){
			if (errno == EAGAIN || errno == EWOULDBLOCK)
				return (printf("Request timeout for icmp_seq %d\n", config->sequence - 1), 1);
			perror("ft_ping: recvfrom");
			return (1);
		}
		gettimeofday(&recv_time, NULL);
		ip_hdr = (struct ip *)buffer;
		ip_hdr_len = ip_hdr->ip_hl << 2;
		icmp_hdr = (struct icmp *)(buffer + ip_hdr_len);
		if (icmp_hdr->icmp_type != ICMP_ECHOREPLY){
			if (icmp_hdr->icmp_type != ICMP_ECHO && config->verbose){
				// Los errores ICMP (type=11, type=3...) encapsulan el header IP+ICMP
				// original. Hay que navegar hasta él para obtener el icmp_seq real.
				struct ip	*orig_ip   = (struct ip *)((char *)icmp_hdr + 8);
				struct icmp	*orig_icmp = (struct icmp *)((char *)orig_ip + (orig_ip->ip_hl << 2));
				printf("From %s: icmp_seq=%d type=%d code=%d\n",
					inet_ntoa(addr.sin_addr),
					orig_icmp->icmp_seq,
					icmp_hdr->icmp_type,
					icmp_hdr->icmp_code);
			}
			continue;
		}
		if (icmp_hdr->icmp_id != (getpid() & 0xFFFF)){
			if (config->verbose)
				printf("Received reply for different process\n");
			continue;
		}
		break;
	}
	rtt = (recv_time.tv_sec - send_time->tv_sec) * 1000.0 + (recv_time.tv_usec - send_time->tv_usec) / 1000.0;
	config->stats.packets_received++;
	if (config->stats.packets_received == 1 || rtt < config->stats.min_rtt)
		config->stats.min_rtt = rtt;
	if (config->stats.packets_received == 1 || rtt > config->stats.max_rtt)
		config->stats.max_rtt = rtt;
	config->stats.sum_rtt += rtt;
	config->stats.sum_sq_rtt += rtt * rtt;
	printf("%d bytes from %s: icmp_seq=%d ttl=%d time=%.3f ms\n",
		bytes_received - ip_hdr_len,
		config->no_dns ? config->resolved_ip : config->target,
		icmp_hdr->icmp_seq, ip_hdr->ip_ttl, rtt);
	return (0);
}
