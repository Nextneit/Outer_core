#include "../include/ft_ping.h"

void	print_help(void)
{
	printf("Usage: ft_ping [OPTION...] HOST\n");
	printf("Send ICMP ECHO_REQUEST packets to network hosts.\n\n");
	printf("Options:\n");
	printf("  -v              verbose output\n");
	printf("  -n              no DNS lookup on reply, show IP only\n");
	printf("  -s SIZE         number of data bytes to send (default: 56)\n");
	printf("  --ttl TTL       define time to live (1-255)\n");
	printf("  -W TIMEOUT      time in ms to wait for a reply (default: 1000)\n");
	printf("  -w DEADLINE     total time in seconds before ft_ping exits\n");
	printf("  -?              give this help list\n\n");
	printf("Report bugs to <your_email@example.com>.\n");
}

static int	parse_options(int argc, char **argv, t_ping_config *config, int target){
	int	i;

	i = 1;
	// Valores por defecto: equivalentes a los de inetutils-2.0
	config->verbose     = false;
	config->no_dns      = false;             	// por defecto muestra hostname
	config->ttl         = DEFAULT_TTL;       	// 64, valor estándar en Linux
	config->packet_size = PACKET_SIZE - 8;   	// 56 bytes de datos (64 - 8 cabecera ICMP)
	config->timeout_ms  = RECV_TIMEOUT * 1000;	// 1000ms = 1s de espera por paquete
	config->deadline    = 0;                 	// 0 = sin límite de tiempo total
	target = -1;
	while (i < argc){
		if (argv[i][0] == '-'){
			// -v: muestra errores ICMP y detalles de paquetes descartados
			if (strncmp(argv[i], "-v", strlen(argv[i])) == 0)
				config->verbose = true;
			// -n: suprime la resolución inversa DNS en la salida, útil en redes
			//     donde el DNS inverso es lento o no está disponible
			else if (strncmp(argv[i], "-n", strlen(argv[i])) == 0)
				config->no_dns = true;
			// --ttl: Time To Live del paquete IP. Cada router decrementa 1.
			//        Rango 1-255: campo de 8 bits en la cabecera IP.
			//        Útil para forzar errores ICMP_TIMXCEED (type=11) con TTL bajo.
			else if (strncmp(argv[i], "--ttl", strlen(argv[i])) == 0)
			{
				if (i + 1 >= argc)
					return (printf("ft_ping: option requires an argument -- '--ttl'\n"), 1);
				config->ttl = atoi(argv[++i]);
				if (config->ttl <= 0 || config->ttl > 255)
					return (printf("ft_ping: invalid TTL value\n"), 1);
			}
			// -s: bytes de datos del payload ICMP (sin contar la cabecera ICMP de 8 bytes).
			//     Máximo 65507 = 65535 (UDP max) - 20 (IP header) - 8 (ICMP header).
			else if (strncmp(argv[i], "-s", strlen(argv[i])) == 0)
			{
				if (i + 1 >= argc)
					return (printf("ft_ping: option requires an argument -- '-s'\n"), 1);
				config->packet_size = atoi(argv[++i]);
				if (config->packet_size < 0 || config->packet_size > 65507)
					return (printf("ft_ping: invalid packet size\n"), 1);
			}
			// -W: tiempo máximo en milisegundos que se espera la respuesta de UN paquete.
			//     Controla SO_RCVTIMEO del socket. Si expira → "Request timeout".
			else if (strncmp(argv[i], "-W", strlen(argv[i])) == 0)
			{
				if (i + 1 >= argc)
					return (printf("ft_ping: option requires an argument -- '-W'\n"), 1);
				config->timeout_ms = atoi(argv[++i]);
				if (config->timeout_ms <= 0)
					return (printf("ft_ping: invalid timeout\n"), 1);
			}
			// -w: deadline total en segundos. El programa termina aunque haya
			//     paquetes pendientes. Se compara contra start_time en el loop principal.
			else if (strncmp(argv[i], "-w", strlen(argv[i])) == 0)
			{
				if (i + 1 >= argc)
					return (printf("ft_ping: option requires an argument -- '-w'\n"), 1);
				config->deadline = atoi(argv[++i]);
				if (config->deadline <= 0)
					return (printf("ft_ping: invalid deadline\n"), 1);
			}
			else if (strncmp(argv[i], "-?", strlen(argv[i])) == 0
				|| strncmp(argv[i], "--help", strlen(argv[i])) == 0){
				print_help();
				exit(0);
			}
			else
				return (printf("ft_ping: invalid option '%s'\n", argv[i]), 1);
		}
		else{
			if (target != -1)
				return (printf("ft_ping: too many arguments\n"), 1);
			target = i;
			config->target = argv[i];
		}
		i++;
	}
	if (config->target == NULL)
		return (printf("Error: missing host operand\n"), 1);
	return (0);
}

int	parse_arguments(int argc, char **argv, t_ping_config *config){
	int	target;
	
	target = -1;
	if (argc < 2)
		return (printf("Error: missing host operand\n"), 1);
	if (parse_options(argc, argv, config, target) == 1)
		return (1);
	return (0);
}
