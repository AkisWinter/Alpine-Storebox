FROM alpine:3.18

LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL Author="AkisWinter"
LABEL Email="a@a.com"
LABEL version="0.1"
LABEL description="simple Alpine Docker container enabling SSH access points for\
                   repositories and data storage."

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