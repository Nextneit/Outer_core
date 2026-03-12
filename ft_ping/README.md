# ft_ping

Reimplementación del comando `ping` en C usando **sockets RAW** e **ICMP**. Proyecto de la escuela 42.

## Índice
- [Compilación y Uso](#compilación-y-uso)
- [Opciones](#opciones)
- [Arquitectura](#arquitectura)
- [Conceptos Fundamentales](#conceptos-fundamentales)
- [Módulos](#módulos)
- [Ejecutar con Valgrind](#ejecutar-con-valgrind)

---

## Compilación y Uso

### Compilar
```bash
make
```
El Makefile compila el binario y establece automáticamente la capability `cap_net_raw` para permitir sockets RAW sin necesidad de ejecutar como root.

### Uso básico
```bash
./ft_ping google.com
./ft_ping 8.8.8.8
./ft_ping -v 42.fr
./ft_ping -s 128 --ttl 32 -w 5 google.com
```

### Limpiar
```bash
make clean     # Elimina objetos
make fclean    # Elimina objetos y binario
make re        # Recompila desde cero
make debug     # Compila con AddressSanitizer, UBSan y flag DEBUG (sin capabilities)
```

---

## Opciones

| Opción | Descripción |
|--------|-------------|
| `-v` | Modo verbose: muestra paquetes enviados y respuestas no solicitadas |
| `-n` | No resuelve DNS inverso en la salida; muestra solo la IP |
| `-s SIZE` | Bytes de datos del payload ICMP (default: 56, máx: 65507) |
| `--ttl TTL` | Time To Live del paquete IP (rango: 1–255, default: 64) |
| `-W TIMEOUT` | Tiempo máximo en ms de espera por la respuesta de un paquete (default: 1000) |
| `-w DEADLINE` | Tiempo total en segundos antes de que ft_ping termine (0 = sin límite) |
| `-?` / `--help` | Muestra la ayuda |

---

## Arquitectura

```
ft_ping/
├── include/
│   └── ft_ping.h         # Definiciones, structs y prototipos
└── src/
    ├── main.c            # Punto de entrada y bucle principal
    ├── parse.c           # Parseo de argumentos y opciones
    ├── dns.c             # Resolución de hostname a IP
    ├── icmp.c            # Construcción y checksum del paquete ICMP
    ├── network.c         # Socket RAW, envío y recepción de paquetes
    ├── signals.c         # Manejador de SIGINT (Ctrl+C)
    └── statistics.c      # Cálculo e impresión de estadísticas finales
```

### Structs Principales

```c
typedef struct s_ping_stats {
    uint64_t    packets_sent;
    uint64_t    packets_received;
    double      min_rtt;
    double      max_rtt;
    double      sum_rtt;
    double      sum_sq_rtt;   // Para calcular la desviación estándar (mdev)
} t_ping_stats;

typedef struct s_ping_config {
    char            *target;                       // Hostname o IP introducido
    char            resolved_ip[INET_ADDRSTRLEN];  // IP resuelta
    bool            verbose;                       // Flag -v
    bool            no_dns;                        // Flag -n
    int             sockfd;                        // File descriptor del socket
    int             ttl;                           // TTL del paquete IP (--ttl)
    int             packet_size;                   // Bytes de datos ICMP (-s)
    int             timeout_ms;                    // Timeout por paquete en ms (-W)
    int             deadline;                      // Deadline total en segundos (-w)
    uint16_t        sequence;                      // Número de secuencia ICMP
    t_ping_stats    stats;                         // Estadísticas de la sesión
    struct timeval  start_time;                    // Tiempo de inicio
} t_ping_config;
```

---

## Conceptos Fundamentales

### ¿Qué es ICMP?

El **Internet Control Message Protocol (ICMP)** es un protocolo de red que opera sobre IP. `ping` usa dos tipos de mensajes:

- **ICMP Echo Request** (`type=8`): el paquete que enviamos
- **ICMP Echo Reply** (`type=0`): la respuesta del host remoto

### Estructura del Paquete ICMP

```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|     Type      |     Code      |          Checksum             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Identifier          |        Sequence Number        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data...                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

- **Identifier**: PID del proceso (`getpid() & 0xFFFF`) para distinguir respuestas propias
- **Sequence**: número incremental por cada paquete enviado
- **Data**: bytes de relleno cuyo tamaño se controla con `-s` (default: 56)

### Sockets RAW

A diferencia de TCP/UDP, los **sockets RAW** permiten construir paquetes a nivel IP/ICMP manualmente:

```c
sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
```

Requieren privilegios elevados. Se gestiona vía **Linux capabilities**:
```bash
sudo setcap cap_net_raw+ep ft_ping
```
Esto evita ejecutar el binario completo como root.

### Cálculo del RTT

El **Round-Trip Time** se calcula midiendo el tiempo entre `sendto` y `recvfrom`:

```c
rtt = (recv_time.tv_sec  - send_time->tv_sec)  * 1000.0
    + (recv_time.tv_usec - send_time->tv_usec) / 1000.0;
```

El resultado se expresa en **milisegundos**.

### Desviación Estándar (mdev)

Al final de la sesión se calcula la desviación media del RTT usando la fórmula de varianza:

```
mdev = sqrt( sum(rtt²)/n  -  (sum(rtt)/n)² )
```

---

## Módulos

### `main.c` — Bucle Principal

1. Parsea argumentos con `parse_arguments()`
2. Resuelve el hostname con `resolve_hostname()`
3. Crea el socket RAW con `create_raw_socket()`
4. Registra el manejador de señales con `setup_signal_handlers()`
5. Entra en el bucle: envía ping → recibe respuesta → espera 1 segundo
6. Respeta el deadline (`-w`) si está definido

### `parse.c` — Argumentos

- Acepta `-v`, `-n`, `-s`, `--ttl`, `-W`, `-w` y `-?`/`--help`
- Rechaza opciones desconocidas con mensaje de error
- Valida que se haya indicado exactamente un host
- Valores por defecto equivalentes a `inetutils-2.0`

### `dns.c` — Resolución DNS

Usa `getaddrinfo()` con `AF_INET` para resolver el hostname a IPv4 y almacena la IP en formato cadena con `inet_ntop()`. Libera correctamente el resultado con `freeaddrinfo()`.

### `icmp.c` — Paquetes ICMP

**`create_icmp_packet()`**:
- Inicializa el paquete a cero (`memset`)
- Rellena cabecera ICMP: type, code, id (PID), sequence
- Rellena payload con bytes incrementales
- Calcula y asigna el checksum

**`calculate_checksum()`**:
- Algoritmo de complemento a uno sobre palabras de 16 bits
- Estándar RFC 792 para verificar integridad del paquete

### `network.c` — Red

**`create_raw_socket()`**:
- Crea socket `SOCK_RAW`/`IPPROTO_ICMP`
- Configura TTL vía `setsockopt(IP_TTL)` (default 64, sobreescribible con `--ttl`)
- Configura timeout de recepción vía `setsockopt(SO_RCVTIMEO)` (controlado por `-W`)

**`send_ping()`**:
- Construye dirección de destino con `inet_pton`
- Llama a `create_icmp_packet()` y envía con `sendto`
- Incrementa `packets_sent` y `sequence`

**`receive_ping()`**:
- Lee respuesta con `recvfrom`
- Salta la cabecera IP (`ip_hl << 2`) para acceder al ICMP
- Verifica `type == ICMP_ECHOREPLY` e `id == PID`
- Calcula RTT y actualiza estadísticas (min, max, sum, sum²)
- Imprime: `N bytes from IP: icmp_seq=X ttl=Y time=Z ms`

### `signals.c` — Señales

**`setup_signal_handlers()`**:
- Guarda un puntero global a `t_ping_config`
- Registra `handle_sigint` para `SIGINT` (Ctrl+C)

**`handle_sigint()`**:
- Llama a `print_statistics()` antes de salir
- Cierra el socket y libera la memoria del config

### `statistics.c` — Estadísticas

**`print_statistics()`**:
- Calcula el tiempo total transcurrido desde `start_time`
- Imprime el porcentaje de pérdida de paquetes
- Si se recibió al menos una respuesta, imprime `rtt min/avg/max/mdev`

---

## Ejecutar con Valgrind

Los sockets RAW requieren la capability `cap_net_raw`. Valgrind **no puede** heredar capabilities de un binario con `setcap`, por lo que el flujo correcto es:

### 1. Quitar las capabilities del binario
```bash
/sbin/setcap -r ./ft_ping
```

### 2. Ejecutar Valgrind con privilegios de root
```bash
# Leak check básico
sudo valgrind --leak-check=full ./ft_ping -v localhost

# Leak check completo con seguimiento de orígenes
sudo valgrind \
  --leak-check=full \
  --show-leak-kinds=all \
  --track-origins=yes \
  ./ft_ping -v localhost

# Con deadline para terminar automáticamente en N segundos
sudo valgrind \
  --leak-check=full \
  --show-leak-kinds=all \
  --track-origins=yes \
  ./ft_ping -v -w 3 localhost
```

### 3. Restaurar las capabilities
```bash
sudo setcap cap_net_raw+ep ./ft_ping
```

> **Nota**: La memoria clasificada como `still reachable` en los resultados de Valgrind es normal y corresponde a buffers internos de `getaddrinfo()` de la libc que se liberan al finalizar el proceso.
