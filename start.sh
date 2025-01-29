#!/bin/bash

start_wireguard_configs() {
    local WG_CONFIG_DIR="/etc/wireguard"

    if [ -d "$WG_CONFIG_DIR" ]; then
        local conf_files=("$WG_CONFIG_DIR"/*.conf)
        if [ ${#conf_files[@]} -eq 0 ]; then
            echo "No WireGuard configuration files found in $WG_CONFIG_DIR"
            return 1
        fi

        for conf_file in "${conf_files[@]}"; do
            if [ -f "$conf_file" ]; then
                local interface
                interface=$(basename "$conf_file" .conf)
                echo "Starting WireGuard interface: $interface"
                wg-quick up "$interface"
            fi
        done
    else
        echo "Directory $WG_CONFIG_DIR does not exist"
        return 1
    fi

    echo "All WireGuard interfaces started successfully"
    return 0
}

start_setup_py() {
    # create user from yaml
    python /setup.py /config/users.yaml
}

start_sshd_with_config() {
    local SSHD_CONFIG_FILE="/etc/ssh/sshd_config"

    if [ -f "$SSHD_CONFIG_FILE" ]; then
        echo "Starting SSH daemon (sshd) with the specified configuration file: $SSHD_CONFIG_FILE"
        /usr/sbin/sshd -f "$SSHD_CONFIG_FILE" -D
    else
        echo "SSHD configuration file $SSHD_CONFIG_FILE not found"
        return 1
    fi

    return 0
}

start_fail2ban() {
    echo "Starting Fail2Ban"
    fail2ban-server -xf start
}

start_rsyslog() {
    echo "Starting rsyslog"
    cp /defaults/rsyslog.conf /etc/rsyslog.conf
    rsyslogd &
}

update_sshkeys() {
    echo "Updating SSH keys"
    python /update_sshkeys.py /config/users.yaml
}
# Call the function
start_rsyslog
start_setup_py
start_wireguard_configs
sleep 5
start_sshd_with_config
start_fail2ban

echo "All processes started successfully"

while true
do
    sleep 30
    update_sshkeys
done
}