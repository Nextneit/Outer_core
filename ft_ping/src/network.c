#include "../include/ft_ping.h"

int create_raw_socket(void){
	int		sockfd;
	int		ttl;
	struct	timeval timeout;

	ttl = DEFAULT_TTL;
	sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
	if (sockfd < 0){
		if (errno == EPERM)
			printf("ft_ping: socket: Operation not permitted\n");
		else
			perror("ft_ping: socket");
		return (-1);
	}
	if (setsockopt(sockfd, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl)) < 0){
		perror("ft_ping: setsockoptTTL");
		close(sockfd);
		return (-1);
	}
	timeout.tv_sec = RECV_TIMEOUT;
	timeout.tv_usec = 0;
	if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) < 0){
		perror("ft_ping: setsockopt timeout");
		close(sockfd);
		return (-1);
	}
	return (sockfd);
}

int	send_ping(t_ping_config *config){
	char	packet[PACKET_SIZE];
	struct	sockaddr_in addr;
	int		bytes_sent;

	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;
	inet_pton(AF_INET, config->resolved_ip, &addr.sin_addr);
	create_icmp_packet(packet, config->sequence);
	bytes_sent = sendto(config->sockfd, packet, PACKET_SIZE, 0, (struct sockaddr *)&addr, sizeof(addr));
	if (bytes_sent < 0)
		return (perror("ft_ping: sendto"), 1);
	config->stats.packets_sent++;
	config->sequence++;
	if (config->verbose)
		printf("Sent ICMP packet: seq=%d, bytes=%d\n", config->sequence - 1, bytes_sent);
	return (0);
}

int	receive_ping(t_ping_config *config, struct timeval *send_time){
	char buffer[1024];
    struct sockaddr_in addr;
    socklen_t addr_len;
    struct timeval recv_time;
    int bytes_received;
    struct ip *ip_hdr;
    struct icmp *icmp_hdr;
    int ip_hdr_len;
    double rtt;

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
		if (config->verbose)
			printf("Received non-echo reply (type=%d)\n", icmp_hdr->icmp_type);
		return (1);
	}
	if (icmp_hdr->icmp_id != (getpid() & 0xFFFF)){
		if (config->verbose)
			printf("Received reply for different proccess\n");
		return (1);
	}
	rtt = (recv_time.tv_sec - send_time->tv_sec) * 1000.0 + (recv_time.tv_usec - send_time->tv_usec) / 1000.0;
	config->stats.packets_received++;
    if (config->stats.packets_received == 1 || rtt < config->stats.min_rtt)
        config->stats.min_rtt = rtt;
    if (config->stats.packets_received == 1 || rtt > config->stats.max_rtt)
        config->stats.max_rtt = rtt;
    config->stats.sum_rtt += rtt;
    config->stats.sum_sq_rtt += rtt * rtt;
    printf("%d bytes from %s: icmp_seq=%d ttl=%d time=%.3f ms\n", bytes_received - ip_hdr_len, config->resolved_ip, icmp_hdr->icmp_seq, ip_hdr->ip_ttl, rtt);
	return (0);
}