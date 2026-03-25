# ft_ping

C implementation of the `ping` command using **RAW sockets** and **ICMP**. School 42 project.

## Index
- [Compilation and Usage](#compilation-and-usage)
- [Options](#options)
- [Architecture](#architecture)
- [Fundamental Concepts](#fundamental-concepts)
- [Modules](#modules)
- [Running with Valgrind](#running-with-valgrind)

---

## Compilation and Usage

### Compile
```bash
make
```
The Makefile compiles the binary and automatically sets the `cap_net_raw` capability to allow RAW sockets without needing to run as root.

### Basic usage
```bash
./ft_ping google.com
./ft_ping 8.8.8.8
./ft_ping -v 42.fr
./ft_ping -s 128 --ttl 32 -w 5 google.com
```

### Clean
```bash
make clean     # Remove object files
make fclean    # Remove object files and binary
make re        # Recompile from scratch
make debug     # Compile with AddressSanitizer, UBSan and DEBUG flag (no capabilities)
```

---

## Options

| Option | Description |
|--------|-------------|
| `-v` | Verbose mode: show sent packets and unsolicited responses |
| `-n` | Do not resolve reverse DNS in output; show IP only |
| `-s SIZE` | Bytes of ICMP payload data (default: 56, max: 65507) |
| `--ttl TTL` | Time To Live of the IP packet (range: 1–255, default: 64) |
| `-W TIMEOUT` | Maximum time in ms to wait for packet response (default: 1000) |
| `-w DEADLINE` | Total time in seconds before ft_ping terminates (0 = unlimited) |
| `-?` / `--help` | Show help |

---

## Architecture

```
ft_ping/
├── include/
│   └── ft_ping.h         # Definitions, structs and prototypes
└── src/
    ├── main.c            # Entry point and main loop
    ├── parse.c           # Argument and option parsing
    ├── dns.c             # Hostname to IP resolution
    ├── icmp.c            # ICMP packet construction and checksum
    ├── network.c         # RAW socket, packet send and receive
    ├── signals.c         # SIGINT handler (Ctrl+C)
    └── statistics.c      # Calculate and print final statistics
```

### Main Structs

```c
typedef struct s_ping_stats {
    uint64_t    packets_sent;
    uint64_t    packets_received;
    double      min_rtt;
    double      max_rtt;
    double      sum_rtt;
    double      sum_sq_rtt;   // To calculate standard deviation (mdev)
} t_ping_stats;

typedef struct s_ping_config {
    char            *target;                       // Hostname or IP entered
    char            resolved_ip[INET_ADDRSTRLEN];  // Resolved IP
    bool            verbose;                       // Flag -v
    bool            no_dns;                        // Flag -n
    int             sockfd;                        // Socket file descriptor
    int             ttl;                           // TTL of IP packet (--ttl)
    int             packet_size;                   // Bytes of ICMP data (-s)
    int             timeout_ms;                    // Per-packet timeout in ms (-W)
    int             deadline;                      // Total deadline in seconds (-w)
    uint16_t        sequence;                      // ICMP sequence number
    t_ping_stats    stats;                         // Session statistics
    struct timeval  start_time;                    // Start time
} t_ping_config;
```

---

## Fundamental Concepts

### What is ICMP?

The **Internet Control Message Protocol (ICMP)** is a network protocol that operates on top of IP. `ping` uses two types of messages:

- **ICMP Echo Request** (`type=8`): the packet we send
- **ICMP Echo Reply** (`type=0`): the response from the remote host

### ICMP Packet Structure

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

- **Identifier**: Process PID (`getpid() & 0xFFFF`) to distinguish own responses
- **Sequence**: incremental number for each packet sent
- **Data**: padding bytes whose size is controlled with `-s` (default: 56)

### RAW Sockets

Unlike TCP/UDP, **RAW sockets** allow manually constructing IP/ICMP packets:

```c
sockfd = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP);
```

They require elevated privileges. Managed via **Linux capabilities**:
```bash
sudo setcap cap_net_raw+ep ft_ping
```
This avoids running the entire binary as root.

### RTT Calculation

The **Round-Trip Time** is calculated by measuring the time between `sendto` and `recvfrom`:

```c
rtt = (recv_time.tv_sec  - send_time->tv_sec)  * 1000.0
    + (recv_time.tv_usec - send_time->tv_usec) / 1000.0;
```

The result is expressed in **milliseconds**.

### Standard Deviation (mdev)

At the end of the session, the mean deviation of RTT is calculated using the variance formula:

```
mdev = sqrt( sum(rtt²)/n  -  (sum(rtt)/n)² )
```

---

## Modules

### `main.c` — Main Loop

1. Parses arguments with `parse_arguments()`
2. Resolves hostname with `resolve_hostname()`
3. Creates RAW socket with `create_raw_socket()`
4. Registers signal handler with `setup_signal_handlers()`
5. Enters loop: send ping → receive response → wait 1 second
6. Respects the deadline (`-w`) if defined

### `parse.c` — Arguments

- Accepts `-v`, `-n`, `-s`, `--ttl`, `-W`, `-w` and `-?`/`--help`
- Rejects unknown options with error message
- Validates that exactly one host has been specified
- Default values equivalent to `inetutils-2.0`

### `dns.c` — DNS Resolution

Uses `getaddrinfo()` with `AF_INET` to resolve hostname to IPv4 and stores the IP in string format with `inet_ntop()`. Correctly releases the result with `freeaddrinfo()`.

### `icmp.c` — ICMP Packets

**`create_icmp_packet()`**:
- Initializes packet to zero (`memset`)
- Fills ICMP header: type, code, id (PID), sequence
- Fills payload with incremental bytes
- Calculates and assigns checksum

**`calculate_checksum()`**:
- One's complement algorithm on 16-bit words
- RFC 792 standard to verify packet integrity

### `network.c` — Network

**`create_raw_socket()`**:
- Creates `SOCK_RAW`/`IPPROTO_ICMP` socket
- Configures TTL via `setsockopt(IP_TTL)` (default 64, overridable with `--ttl`)
- Configures receive timeout via `setsockopt(SO_RCVTIMEO)` (controlled by `-W`)

**`send_ping()`**:
- Builds destination address with `inet_pton`
- Calls `create_icmp_packet()` and sends with `sendto`
- Increments `packets_sent` and `sequence`

**`receive_ping()`**:
- Reads response with `recvfrom`
- Skips IP header (`ip_hl << 2`) to access ICMP
- Verifies `type == ICMP_ECHOREPLY` and `id == PID`
- Calculates RTT and updates statistics (min, max, sum, sum²)
- Prints: `N bytes from IP: icmp_seq=X ttl=Y time=Z ms`

### `signals.c` — Signals

**`setup_signal_handlers()`**:
- Saves a global pointer to `t_ping_config`
- Registers `handle_sigint` for `SIGINT` (Ctrl+C)

**`handle_sigint()`**:
- Calls `print_statistics()` before exiting
- Closes socket and frees config memory

### `statistics.c` — Statistics

**`print_statistics()`**:
- Calculates total elapsed time since `start_time`
- Prints packet loss percentage
- If at least one response was received, prints `rtt min/avg/max/mdev`

---

## Running with Valgrind

RAW sockets require the `cap_net_raw` capability. Valgrind **cannot** inherit capabilities from a binary with `setcap`, so the correct workflow is:

### 1. Remove capabilities from the binary
```bash
/sbin/setcap -r ./ft_ping
```

### 2. Run Valgrind with root privileges
```bash
# Basic leak check
sudo valgrind --leak-check=full ./ft_ping -v localhost

# Full leak check with origin tracking
sudo valgrind \
  --leak-check=full \
  --show-leak-kinds=all \
  --track-origins=yes \
  ./ft_ping -v localhost

# With deadline to auto-terminate in N seconds
sudo valgrind \
  --leak-check=full \
  --show-leak-kinds=all \
  --track-origins=yes \
  ./ft_ping -v -w 3 localhost
```

### 3. Restore capabilities
```bash
sudo setcap cap_net_raw+ep ./ft_ping
```

> **Note**: Memory marked as `still reachable` in Valgrind results is normal and corresponds to internal buffers from `getaddrinfo()` in libc that are freed when the process exits.
