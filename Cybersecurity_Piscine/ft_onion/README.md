# ft_onion

A Tor hidden service exposing a static web page over HTTP and accessible via SSH, fully containerized with Docker.

---

## Overview

This project deploys three services inside a single Docker container:

| Service | Port | Description |
|---------|------|-------------|
| **Nginx** | `80` (internal) | Serves the static `index.html` |
| **Tor** | — | Exposes the web page as a `.onion` hidden service |
| **OpenSSH** | `4242` | Remote access to the container |

> Nginx is not exposed directly to the host. External access to the web page is exclusively through the Tor network via a `.onion` address.

---

## Requirements

- Docker

---

## Usage

### Build and run

```bash
docker build -t ft_onion .
docker run -p 4242:4242 ft_onion
```

Or with Docker Compose:

```bash
docker compose up --build
```

### Retrieve the .onion address

Once the container is running, wait ~30–60 seconds for Tor to bootstrap, then:

```bash
docker compose exec ft_onion cat /var/lib/tor/hidden_service/hostname
```

Open the resulting `.onion` address in **Tor Browser**.

### SSH access

```bash
ssh user42@localhost -p 4242
# Password: password
```

---

## Project Structure

```
ft_onion/
├── Dockerfile
├── docker-compose.yml
├── index.html       # Static page served by Nginx
├── nginx.conf       # Nginx configuration (port 80, static root)
├── sshd_config      # SSH on port 4242, root login disabled
└── torrc            # Hidden service pointing to 127.0.0.1:80
```

---

## Network Architecture

```
Tor Network ──→ .onion:80 ──→ tor daemon ──→ 127.0.0.1:80 ──→ nginx ──→ index.html
SSH Client  ──→ host:4242 ──→ sshd ──→ user42
```

---

## Security Considerations

- Root login is disabled (`PermitRootLogin no` in `sshd_config`)
- No host firewall rules are added
- Tor handles all inbound web traffic — no HTTP port is exposed to the host
- The container runs on `debian:bookworm-slim` to minimize the attack surface
