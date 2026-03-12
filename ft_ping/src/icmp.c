#include "../include/ft_ping.h"

uint16_t	calculate_checksum(uint16_t *addr, int len){
	uint32_t	sum;
	uint16_t	*w;
	uint16_t	answer;
	int			nleft;

	sum = 0;
	w = addr;
	answer = 0;
	nleft = len;
	while (nleft > 1){
		sum += *w++;
		nleft -= 2;
	}
	if (nleft == 1){
		*(unsigned char *)(&answer) = *(unsigned char *)w;
		sum += answer;
	}

	sum = (sum >> 16) + (sum & 0xffff);
	sum += (sum >> 16);
	answer = ~sum;
	return (answer);
}

void	create_icmp_packet(char *packet, uint16_t sequence, int size){
	struct icmp *icmp_hdr;
	int			i;
	
	// size = bytes de datos, +8 = cabecera ICMP
	memset(packet, 0, size + 8);
	icmp_hdr = (struct icmp *)packet;
	icmp_hdr->icmp_type = ICMP_ECHO;
	icmp_hdr->icmp_code = 0;
	icmp_hdr->icmp_id = getpid() & 0xFFFF;
	icmp_hdr->icmp_seq = sequence;
	icmp_hdr->icmp_cksum = 0;
	i = sizeof(struct icmp);
	while (i < size + 8){
		packet[i] = i;
		i++;
	}
	icmp_hdr->icmp_cksum = calculate_checksum((uint16_t*)packet, size + 8);
}
