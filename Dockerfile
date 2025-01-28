FROM alpine:3.21

LABEL Author="AkisWinter"
LABEL Email="norman.schmidt90@gmail.com"
LABEL version="v0.4.0"
LABEL description="Docker container that established a SSH access point without password login.\
                  SSH users are initially specified in a YAML file along with their public keys.\
                  Upon container startup, users are created within the system, and their public keys\
                  are placed in the .ssh/authorized_keys file. New SSH public keys can be added or removed via SSH.\
                  Currently, the YAML file is not updated automatically.\
                  SSH, Wireguard, and fail2ban can be easily customized via volumes."

RUN apk update &&\
    apk add --no-cache  bash \
                        wget \
                        shadow \
                        wireguard-tools \
                        openssh \
                        curl \
                        dumb-init \
                        python3 \ 
                        fail2ban \
                        rsyslog \
                        py3-yaml \
                        iproute2 \
                        iptables \
                        ip6tables \
                        iputils \
                        libcap-utils \
                        borgbackup \
                        net-tools && \
    mkdir /root/.ssh && \
    mkdir /run/sshd && \
    mkdir /config && \
    mkdir /defaults && \
    mkdir /defaults/config && \
    mkdir /defaults/ssh && \
    mkdir /defaults/fail2ban && \
    rm -rf /var/cache/apk/*

COPY defaults /defaults
COPY setup.py /setup.py
COPY start.sh /start.sh
EXPOSE 2223
EXPOSE 51820

#volume
VOLUME /config
VOLUME /etc/ssh
VOLUME /etc/wireguard
VOLUME /etc/fail2ban
VOLUME /home
VOLUME /var/log

ENTRYPOINT ["/usr/bin/dumb-init","/start.sh"]
