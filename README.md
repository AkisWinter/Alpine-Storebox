# Alpine-Storebox
Docker container that established a SSH access point without password login.

SSH users are initially specified in a YAML file along with their public keys. Upon container startup, users are created within the system, and their public keys are placed in the .ssh/authorized_keys file. New SSH public keys can be added or removed via SSH. Currently, the YAML file is not updated automatically.

SSH, Wireguard, and fail2ban can be easily customized via volumes.

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

Starts with the Container, is configured for the SSH port 2223.

Standard configuration adapted according to the wiki
[Alpine-Wiki](https://wiki.alpinelinux.org/wiki/Fail2ban)

## SSH

Todo: - ChrootDirectory
      - Key rotation (From autorized_keys to YAML-File)
      
## Wireguard

All configuration files (*.conf) within the Wireguard folder should be loaded upon container startup.

Todo: Testing


