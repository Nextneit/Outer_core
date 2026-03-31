FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-scapy \
    tcpdump \
    ftp \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

COPY inquisitor.py /usr/local/bin/inquisitor
RUN chmod +x /usr/local/bin/inquisitor
