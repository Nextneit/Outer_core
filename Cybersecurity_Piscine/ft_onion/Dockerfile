FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    nginx \
    tor \
    openssh-server \
	curl \
    && rm -rf /var/lib/apt/lists/* \
	&& mkdir -p /run/sshd \
    && mkdir -p /scripts

COPY nginx.conf   /etc/nginx/nginx.conf
COPY sshd_config  /etc/ssh/sshd_config
COPY torrc        /etc/tor/torrc
COPY index.html   /var/www/html/index.html
COPY init.sh      /scripts

RUN useradd -m -s /bin/bash user42 && \
    echo "user42:password" | chpasswd

RUN ssh-keygen -A

RUN mkdir -p /var/lib/tor/hidden_service && \
    chown -R debian-tor:debian-tor /var/lib/tor/hidden_service && \
    chmod 700 /var/lib/tor/hidden_service && \
    chmod +x ./scripts/init.sh

EXPOSE 4242
EXPOSE 80

CMD ["./scripts/init.sh"]