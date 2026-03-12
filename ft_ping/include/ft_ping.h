#ifndef FT_PING_H
# define FT_PING_H

// Includes estandar
# include <stdio.h>      // printf, fprintf, perror
# include <stdlib.h>     // exit, malloc, free
# include <string.h>     // strncmp, strcmp, strlen, memset, memcpy, strncpy
# include <stdbool.h>    // bool, true, false
# include <stdint.h>     // uint8_t, uint16_t, uint32_t, uint64_t
# include <unistd.h>     // getpid, getuid
# include <math.h>

// Para sockets y red
# include <sys/socket.h> // socket, setsockopt, sendto, recvfrom
# include <netinet/in.h> // struct sockaddr_in, INADDR_ANY, INET_ADDRSTRLEN
# include <netinet/ip.h> // struct ip
# include <netinet/ip_icmp.h> // struct icmp, ICMP_ECHO, ICMP_ECHOREPLY
# include <arpa/inet.h>  // inet_ntop, inet_pton, inet_addr

// Para resolución DNS
# include <netdb.h>      // gethostbyname, getaddrinfo, freeaddrinfo

// Para señales
# include <signal.h>     // signal, SIGINT, SIGALRM

// Para tiempo y estadísticas
# include <sys/time.h>   // gettimeofday, struct timeval

// Para manejo de errores
# include <errno.h>      // errno

// Macros y constantes
# define PACKET_SIZE 64
# define RECV_TIMEOUT 1
# define DEFAULT_TTL 64

// Estructuras principales
typedef struct s_ping_stats {
    uint64_t    packets_sent;
    uint64_t    packets_received;
    double      min_rtt;
    double      max_rtt;
    double      sum_rtt;
    double      sum_sq_rtt;  // Para desviación estándar
} t_ping_stats;

typedef struct s_ping_config {
    char            *target;        // Hostname o IP
    char            resolved_ip[INET_ADDRSTRLEN];
    bool            verbose;        // -v
    bool            no_dns;         // -n  (no resolver hostname en output)
    int             sockfd;
    int             ttl;            // --ttl (reemplaza DEFAULT_TTL)
    int             packet_size;    // -s   (reemplaza PACKET_SIZE)
    int             timeout_ms;     // -W   (timeout por paquete en ms)
    int             deadline;       // -w   (deadline total en segundos, 0 = sin límite)
    uint16_t        sequence;
    t_ping_stats    stats;
    struct timeval  start_time;
} t_ping_config;

// parser.c
int     parse_arguments(int argc, char **argv, t_ping_config *config);
void    print_help(void);

// icmp.c
void    create_icmp_packet(char *packet, uint16_t sequence, int size);
uint16_t calculate_checksum(uint16_t *addr, int len);

// network.c
int     create_raw_socket(t_ping_config *config);
int     send_ping(t_ping_config *config);
int     receive_ping(t_ping_config *config, struct timeval *send_time);

// dns.c
int     resolve_hostname(const char *hostname, char *ip);

// statistics.c
void    print_statistics(t_ping_config *config);

// signals.c
void    setup_signal_handlers(t_ping_config *config);

#endif
