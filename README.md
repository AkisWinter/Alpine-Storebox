# Alpine-Storebox
Docker container that establishes SSH access points for repositories and data storage.

This container streamlines the management of SSH access, enabling secure connections to repositories and data storage. For added flexibility, configuration folders for SSH, Wireguard, and fail2ban are mounted as volumes, allowing for seamless customization.

## docker compose file

```docker
version: '3.0'

services:
  alpine_storebox:
    image: akiteck/alpine_storebox:latest
    cap_add:
      - NET_ADMIN
    volumes:
      - ./config:/config
      - ./ssh:/etc/ssh
      - ./wireguard:/etc/wireguard
      - ./fail2ban:/etc/fail2ban
      - ./data:/home
      - ./logs:/var/log
    ports:
      - 2223:2223
      - 51820:51820
    restart: unless-stopped
```

## Fail2ban

Standard configuration adapted according to the wiki
[Alpine-Wiki](https://wiki.alpinelinux.org/wiki/Fail2ban)

## SSH

Todo: ChrootDirectory

## Wireguard

Todo: Testing


