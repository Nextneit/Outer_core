MAC_SERVER := $(shell docker exec ftp-server cat /sys/class/net/eth0/address 2>/dev/null)
MAC_CLIENT := $(shell docker exec ftp-client  cat /sys/class/net/eth0/address 2>/dev/null)

IP_SERVER  := 172.20.0.2
IP_CLIENT  := 172.20.0.3

help:
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "  make all            Build and start all containers"
	@echo "  make attack         ARP poisoning + sniff all FTP traffic"
	@echo "  make attack-quiet   ARP poisoning + sniff RETR/STOR only"
	@echo "  make ftp            Open interactive FTP session from client"
	@echo "  make test-transfer  Automated STOR + RETR transfer test"
	@echo "  make arp            Show ARP tables of both victims"
	@echo "  make down           Stop and remove containers"
	@echo "  make clean          Remove containers, images and volumes"
	@echo "  make re             Full rebuild"
	@echo "  make logs           Stream container logs"
	@echo ""
	@echo "Recommended order:"
	@echo "  [terminal 1]  make"
	@echo "  [terminal 1]  make attack"
	@echo "  [terminal 2]  make test-transfer   (or: make ftp)"
	@echo "  [terminal 2]  make arp             (verify poisoning)"
	@echo "  [terminal 1]  Ctrl+C"
	@echo "  [terminal 2]  make arp             (verify restoration)"
	@echo ""

all: up info

up:
	docker compose up --build -d
	@echo ""
	@echo "[*] Waiting for containers to be ready..."
	@sleep 2
	@echo "[*] Installing tools in ftp-client (ftp, iproute2)..."
	@docker exec ftp-client apt-get update -qq && \
		docker exec ftp-client apt-get install -y -qq ftp iproute2 > /dev/null
	@echo "[*] Tools ready."

info:
	@echo ""
	@echo "============================================"
	@echo "  Environment ready"
	@echo "============================================"
	@echo "  ftp-server  $(IP_SERVER)  $(MAC_SERVER)"
	@echo "  ftp-client  $(IP_CLIENT)  $(MAC_CLIENT)"
	@echo "  attacker    172.20.0.4"
	@echo "============================================"
	@echo ""
	@echo "  Run 'make help' for usage guide"
	@echo "============================================"
	@echo ""

attack:
	@if [ -z "$(MAC_SERVER)" ] || [ -z "$(MAC_CLIENT)" ]; then \
		echo "[!] Containers not running. Run 'make' first."; exit 1; \
	fi
	@echo "[*] Starting ARP poisoning attack (verbose)..."
	@echo "[*] $(IP_CLIENT) ($(MAC_CLIENT)) <-> $(IP_SERVER) ($(MAC_SERVER))"
	@echo ""
	docker exec -it attacker python3 /usr/local/bin/inquisitor -v \
		$(IP_CLIENT) $(MAC_CLIENT) $(IP_SERVER) $(MAC_SERVER)

attack-quiet:
	@if [ -z "$(MAC_SERVER)" ] || [ -z "$(MAC_CLIENT)" ]; then \
		echo "[!] Containers not running. Run 'make' first."; exit 1; \
	fi
	@echo "[*] Starting ARP poisoning attack (quiet)..."
	docker exec -it attacker python3 /usr/local/bin/inquisitor \
		$(IP_CLIENT) $(MAC_CLIENT) $(IP_SERVER) $(MAC_SERVER)

ftp:
	@echo "[*] Opening FTP session from client to server..."
	@echo "[*] Credentials: user / password"
	@echo ""
	docker exec -it ftp-client ftp $(IP_SERVER) 21

test-transfer:
	@echo "[*] Preparing test files..."
	@docker exec ftp-server sh -c 'echo "secret content from server" > /home/vsftpd/user/server_file.txt'
	@docker exec ftp-client  sh -c 'echo "secret content from client" > /tmp/client_file.txt'
	@echo "[*] Running STOR (upload) + RETR (download)..."
	@docker exec ftp-client sh -c \
		'printf "user user\npassword\nput /tmp/client_file.txt client_file.txt\nget server_file.txt /tmp/downloaded.txt\nbye\n" \
		| ftp -inv $(IP_SERVER) 21'
	@echo ""
	@echo "[*] Verifying downloaded file on client:"
	@docker exec ftp-client cat /tmp/downloaded.txt

arp:
	@echo "[*] ARP table of ftp-client:"
	@docker exec ftp-client ip neigh
	@echo ""
	@echo "[*] ARP table of ftp-server:"
	@docker exec ftp-server ip neigh

down:
	docker compose down

clean: down
	@echo "[*] Removing project images..."
	@docker compose down --rmi all --volumes 2>/dev/null || true
	@echo "[*] Removing dangling images..."
	@docker image prune -f 2>/dev/null || true
	@echo "[*] Done."

re: down all

logs:
	docker compose logs -f

.PHONY: all up info help attack attack-quiet ftp test-transfer arp down clean re logs