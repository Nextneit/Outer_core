# Inquisitor

An ARP poisoning tool with real-time FTP traffic interception, containerized in a multi-service Docker environment.

---

## Overview

`inquisitor` performs a man-in-the-middle (MITM) attack using ARP cache poisoning in both directions (full duplex). While the attack is active, it intercepts and displays FTP file transfer activity between a client and a server in real time.

Upon termination (`CTRL+C`), the tool automatically restores the ARP tables of both victims to their correct state.

---

## Usage

```bash
python3 inquisitor.py [-v] <IP-src> <MAC-src> <IP-target> <MAC-target>
```

| Parameter | Description |
|-----------|-------------|
| `IP-src` | IP address of the source host (e.g. FTP client) |
| `MAC-src` | MAC address of the source host |
| `IP-target` | IP address of the target host (e.g. FTP server) |
| `MAC-target` | MAC address of the target host |
| `-v` | Verbose mode: display all FTP traffic including login |

### Examples

```bash
# Intercept file transfers only
python3 inquisitor.py 172.20.0.3 02:42:ac:14:00:03 172.20.0.2 02:42:ac:14:00:02

# Verbose mode (shows USER, PASS, and all FTP commands)
python3 inquisitor.py -v 172.20.0.3 02:42:ac:14:00:03 172.20.0.2 02:42:ac:14:00:02
```

---

## Test Environment

The repository includes a fully automated Docker Compose test suite with three containers on an isolated network:

| Container | IP | Role |
|-----------|----|------|
| `ftp-server` | `172.20.0.2` | vsftpd FTP server |
| `ftp-client` | `172.20.0.3` | FTP client (victim) |
| `attacker` | `172.20.0.4` | Runs `inquisitor` |

### Setup and Automation (Makefile)

The `Makefile` simplifies the entire process. You can see the full execution flow by running:

```bash
make help
```

**Common commands:**
```bash
make          # Build and start all containers, install dependencies
make info     # View IPs and MAC addresses of the environment
make ftp      # Open FTP session from client to server
make attack   # Run inquisitor in verbose mode automatically
make arp      # Check ARP tables of client and server
make down     # Stop containers
make clean    # Stop containers, remove volumes and orphans
make re       # clean and rebuild
make logs     # Stream container logs
```

### Manual Execution

```bash
# 1. Get MAC addresses
docker exec ftp-server cat /sys/class/net/eth0/address
docker exec ftp-client cat /sys/class/net/eth0/address

# 2. Launch the attack (Terminal 1)
docker exec -it attacker python3 /usr/local/bin/inquisitor \
    172.20.0.3 <MAC-client> 172.20.0.2 <MAC-server>

# 3. Connect from FTP client (Terminal 2)
docker exec -it ftp-client ftp 172.20.0.2 21
# user: user / password: password

# 4. Verify ARP poisoning
docker exec ftp-client ip neigh
# 172.20.0.2 should show the attacker's MAC address

# 5. Press CTRL+C and verify ARP restoration
docker exec ftp-client ip neigh
# 172.20.0.2 should show its own correct MAC address
```

---

## Project Structure

```
Inquisitor/
├── inquisitor.py       # Main program
├── Dockerfile          # Attacker container image
├── docker-compose.yml  # Three-container test environment
└── Makefile            # Automation: up, down, re, logs
```

---

## Technical Details

- **ARP Poisoning** — Sends crafted ARP reply packets every 2 seconds to both victims simultaneously, redirecting traffic through the attacker
- **FTP Sniffing** — Captures TCP packets on port 21 using Scapy's `sniff()`. In standard mode, filters for `RETR` and `STOR` commands. In verbose mode (`-v`), displays all FTP commands including authentication
- **Cleanup** — On `SIGINT`, sends 5 corrective ARP packets to each victim with the legitimate MAC addresses to restore their caches
- **Threading** — ARP poisoning runs in a background thread while the main thread handles packet sniffing

## Dependencies

- Python 3
- [Scapy](https://scapy.net/) (`python3-scapy`)

> Requires `NET_RAW` and `NET_ADMIN` Linux capabilities (provided by the Docker Compose configuration).
