#include "../include/ft_ping.h"

int	resolve_hostname(const char *hostname, char *ip){
	struct	addrinfo hints;
	struct	addrinfo *res;
	struct	sockaddr_in *addr;
	int		status;

	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_RAW;
	hints.ai_protocol = IPPROTO_ICMP;
	status = getaddrinfo(hostname, NULL, &hints, &res);
	if (status != 0)
		return (printf("ft_ping: %s: %s\n", hostname, gai_strerror(status)), 1);
	addr = (struct sockaddr_in *)res->ai_addr;
	inet_ntop(AF_INET, &(addr->sin_addr), ip, INET_ADDRSTRLEN);
	freeaddrinfo(res);
	return (0);
}