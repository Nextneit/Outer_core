# ft_onion

A Tor hidden service exposing a static web page over HTTP and accessible via SSH, fully containerized with Docker.

---

## Overview

This project deploys three services inside a single Docker container:

| Service | Internal Port | External Port | Description |
|---------|---------------|---------------|-------------|
| **Nginx** | `80` | — | Serves the static `index.html` (Tor only) |
| **Tor** | — | — | Exposes the web page as a `.onion` hidden service |
| **OpenSSH** | `4242` | `2222` | Remote access to the container |

> **Web access:** Nginx is not exposed directly to the host. External HTTP access (port 8080 for testing) is possible via `localhost:8080`, but production access is exclusively through the Tor network via a `.onion` address.

---

## Requirements

- Docker & Docker Compose

---

## Quick Start

```bash
# Build and start the container
make start

# Retrieve the .onion address (wait 30-60 seconds for Tor to bootstrap)
make check

# Test SSH access
make test-ssh
# Username: user42
# Password: password

# Test web server
make test-web

# Stop the container
make stop

# Clean up everything
make clean
```

---

## Available Commands

```bash
make help      # Show all available commands
make start     # Build and start the container
make stop      # Stop the container
make clean     # Remove container and image
make test-ssh  # Test SSH connection (port 2222)
make test-web  # Test web server (port 8080)
make check     # Verify all services and .onion address
```

---

## Manual Build & Run

```bash
docker-compose build
docker-compose up -d
```

### Retrieve the .onion address

Once the container is running:

```bash
docker-compose exec ft_onion cat /var/lib/tor/hidden_service/hostname
```

Open the resulting `.onion` address in **Tor Browser**.

### SSH access

```bash
ssh user42@localhost -p 2222
# Password: password
```

---

## Project Structure

```
ft_onion/
├── Dockerfile           # Container recipe
├── docker-compose.yml   # Port mappings: 8080→80, 2222→4242
├── Makefile             # Build automation
├── index.html           # Static page served by Nginx
├── nginx.conf           # Nginx configuration (port 80)
├── sshd_config          # SSH on port 4242, root login disabled
└── torrc                # Hidden service pointing to 127.0.0.1:80
```

---

## Network Architecture

```
External         Docker Host    Container
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tor Browser  ─→ .onion:80   ──→ tor daemon  ──→ 127.0.0.1:80 ──→ nginx ──→ index.html
SSH Client   ─→ 2222        ──→ sshd:4242  ──→ user42
Test Client  ─→ 8080        ──→ nginx:80
```

**Port Mappings:**
- `8080:80` — For local testing (localhost:8080)
- `2222:4242` — SSH access to container port 4242

---

## Security Considerations

- Root login is disabled (`PermitRootLogin no` in `sshd_config`)
- No explicit firewall rules added (relies on Docker networking)
- Tor handles all production web traffic — direct HTTP access (port-8080) is for testing only
- The `.onion` address is regenerated each time the container starts
- The container runs on `debian:bookworm-slim` to minimize the attack surface
- Private SSH keys are generated inside the container and not exposed to the host
