FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-cryptography \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /root/infection

COPY stockholm.py /root/stockholm
RUN chmod +x /root/stockholm

WORKDIR /root

CMD ["/bin/bash"]
