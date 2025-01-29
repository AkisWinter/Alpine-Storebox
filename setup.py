#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module provides functions for removing duplicates from a list of users.
"""
import os
import sys
import shutil
import subprocess
import random
import string
import yaml


def generate_random_password(length):
    """Generates a random password with the specified length."""
    characters = string.ascii_letters + string.digits
    password = "".join(random.choice(characters) for _ in range(length))
    return password


def remove_duplicates(users):
    """
    Remove duplicates from a list of users based on username, userid, and groupid.

    Args:
        users (list[dict]): A list of dictionaries representing users.
        Each dictionary should have the following keys:
            - 'username' (str): The username of the user.
            - 'userid' (int): The user ID.
            - 'groupid' (int): The group ID.
            - 'sshkeys' (list[str]): A list of SSH keys associated with the user.

    Returns:
        list[dict]: A list of dictionaries representing unique users.
        Each dictionary will have the same keys as the input users.

    Note:
        - The 'sshkeys' list is converted to a tuple to ensure it can be used
          in the duplicate check.
        - If a duplicate user is found, a message will be printed
          indicating the duplicate user's details.

    Example:
        users = [
        {'username': 'user1', 'userid': 1, 'groupid': 2, 'sshkeys': ['key1', 'key2']},
        {'username': 'user2', 'userid': 2, 'groupid': 3, 'sshkeys': ['key3', 'key4']},
        {'username': 'user1', 'userid': 1, 'groupid': 2, 'sshkeys': ['key1', 'key2']},
        {'username': 'user3', 'userid': 3, 'groupid': 4, 'sshkeys': ['key5', 'key6']}
        ]

        unique_users = remove_duplicates(users)
        print(unique_users)
        Output: [
        {'username': 'user1', 'userid': 1, 'groupid': 2, 'sshkeys': ['key1', 'key2']},
        {'username': 'user2', 'userid': 2, 'groupid': 3, 'sshkeys': ['key3', 'key4']},
        {'username': 'user3', 'userid': 3, 'groupid': 4, 'sshkeys': ['key5', 'key6']}
        ]
    """
    unique_users = []
    seen_usernames = set()
    seen_user_ids = set()
    seen_group_ids = set()
    seen_sshkeys = set()
    
    for user in users:
        ssh_keys_tuple = tuple(user["sshkeys"])  # Convert the list to a tuple
        if (
                (user["username"] not in seen_usernames)
                and (user["userid"] not in seen_user_ids)
                and (user["groupid"] not in seen_group_ids)
                and (ssh_keys_tuple not in seen_sshkeys)
        ):  # Use the tuple in the set check
            unique_users.append(user)
            seen_usernames.add(user["username"])
            seen_user_ids.add(user["userid"])
            seen_group_ids.add(user["groupid"])
            seen_sshkeys.add(ssh_keys_tuple)  # Add the tuple to the set
        else:
            print(
                f"Duplicate found for user: {user['username']} "
                f"(username: {user['username']}, userid: {user['userid']}, "
                f"groupid: {user['groupid']})"
            )
    return unique_users


# function to create user
def create_user(username, userid, sshkeys):
    """
    Creates a user with the specified username, userid, groupid, and SSH keys.

    Parameters:
    - username (str): The username of the user to create.
    - userid (int): The user ID of the user to create.
    - groupid (int): The group ID of the user to create.
    - sshkeys (List[str]): A list of SSH keys to add to the user's authorized_keys file.

    Returns:
    - None

    The function checks if a user with the specified username already exists.
    If the user does not exist, it creates the user with the specified username,
    userid, and groupid.
    If the user already exists, the function does nothing.
    After creating the user, the function creates a .ssh directory
    in the user's home directory and sets the correct permissions.
    It then adds the provided SSH keys to the user's authorized_keys file.

    Note:
    This function assumes that the 'useradd', 'mkdir', 'chown', 'chmod', and 'touch'
    commands are available in the environment.

    Example usage:
    create_user("john", 1000, 1000, ["ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD..."])
    """
    
    # generate random password 128 characters long
    random_password = generate_random_password(128)
    
    # user home directory
    home_dir = f"/home/{username}"
    
    # check if user exists
    if os.path.exists(home_dir):
        # Check if user name is already in use, if so, do nothing
        if (
                subprocess.run(
                    ["id", "-u", username],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                ).returncode
                == 0
        ):
            print(f"User {username} already exists.")
            return
        
        # create user if not exists
        subprocess.run(
            [
                "useradd",
                "-u",
                str(userid),
                "-p",
                random_password,
                username,
            ],
            check=True,
        )
        print(f"User {username} created.")
    else:
        # create user if not exists
        subprocess.run(
            [
                "useradd",
                "-m",
                "-d",
                home_dir,
                "-u",
                str(userid),
                "-p",
                random_password,
                username,
            ],
            check=True,
        )
        print(f"User {username} and Homedirectory created.")
        
        # create .ssh directory for user
        
        ssh_dir = f"{home_dir}/.ssh"
        authorized_keys_file = f"{ssh_dir}/authorized_keys"
        
        if not os.path.exists(ssh_dir):
            subprocess.run(["mkdir", ssh_dir], check=True)
            subprocess.run(
                ["chown", "-R", f"{username}:{username}", ssh_dir], check=True
            )
            subprocess.run(["chmod", "700", ssh_dir], check=True)
            subprocess.run(["touch", authorized_keys_file], check=True)
            subprocess.run(
                ["chown", f"{username}:{username}", authorized_keys_file], check=True
            )
            subprocess.run(["chmod", "600", authorized_keys_file], check=True)
            print(f"Created .ssh directory for {username}.")
        
        # add public keys to authorized_keys file
        with open(authorized_keys_file, "a", encoding="utf-8") as auth_keys:
            for sshkey in sshkeys:
                auth_keys.write(sshkey + "\n")
            print(f"Added SSH keys for {username}.")


def create_ssh_directory_for_users(users):
    """
    Creates a .ssh directory for each user in the list of users.

    Parameters:
    - users (list): A list of user dictionaries containing 'username' and 'sshkeys' keys.

    Returns:
    - None

    This function creates a .ssh directory for each user in the list of users.
    It checks if the .ssh directory already exists for the user.
    If the .ssh directory does not exist, it creates it and sets the correct permissions.
    The function also adds the provided SSH keys to the user's authorized_keys file.
    """
    for user in users:
        username = user["username"]
        ssh_dir = f"/home/{username}/.ssh"
        authorized_keys_file = f"{ssh_dir}/authorized_keys"
        
        if not os.path.exists(ssh_dir):
            subprocess.run(["mkdir", ssh_dir], check=True)
            subprocess.run(
                ["chown", f"{username}:{username}", ssh_dir], check=True
            )
            subprocess.run(["chmod", "700", ssh_dir], check=True)
            subprocess.run(["touch", authorized_keys_file], check=True)
            subprocess.run(
                ["chown", f"{username}:{username}", authorized_keys_file], check=True
            )
            subprocess.run(["chmod", "600", authorized_keys_file], check=True)
            print(f"Created .ssh directory for {username}.")
        
        # add public keys to authorized_keys file
        with open(authorized_keys_file, "a", encoding="utf-8") as auth_keys:
            for sshkey in user["sshkeys"]:
                auth_keys.write(sshkey + "\n")
            print(f"Added SSH keys for {username}.")

# generate SSH host keys
def generate_ssh_host_keys():
    """
    Generates SSH host keys if they do not exist.

    This function generates SSH host keys for the following key types: RSA, ECDSA,
    and Ed25519.
    If any of these keys do not exist in the specified key files,
    the function generates them using the `ssh-keygen` command-line tool.

    Parameters:
        None

    Returns:
        None
    """
    ssh_keys = [
        ("rsa", "/etc/ssh/ssh_host_rsa_key"),
        ("ecdsa", "/etc/ssh/ssh_host_ecdsa_key"),
        ("ed25519", "/etc/ssh/ssh_host_ed25519_key"),
    ]
    
    for key_type, key_file in ssh_keys:
        if not os.path.exists(key_file):
            subprocess.run(
                ["ssh-keygen", "-t", key_type, "-f", key_file, "-N", "", "-q"],
                check=True,
            )
            print(f"Generated {key_type} SSH host key.")


# check if SSH host keys exist
def check_ssh_host_keys():
    """
    Checks if SSH host keys exist.

    Returns:
        bool: True if all SSH host keys exist, False otherwise.
    """
    ssh_keys = [
        "/etc/ssh/ssh_host_rsa_key",
        "/etc/ssh/ssh_host_ecdsa_key",
        "/etc/ssh/ssh_host_ed25519_key",
    ]
    
    for key_file in ssh_keys:
        if not os.path.exists(key_file):
            return False
    
    return True


# copy default SSH config
def copy_ssh_default_config():
    """
    Copy the default SSH configuration.

    This function copies the default SSH configuration
    from '/defaults/ssh/' to '/etc/ssh/'.

    Returns:
        None
    """
    shutil.copytree("/defaults/ssh/", "/etc/ssh/", dirs_exist_ok=True)
    print("Copied default SSH config.")


# Check if /config/users.yaml exists.
def check_config():
    """
    Check if /config/users.yaml exists.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists("/config/users.yaml")


# check if /etc/fail2ban/fail2ban.local exists
def check_fail2ban():
    """
    Check if /etc/fail2ban/fail2ban.local exists.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists("/etc/fail2ban/fail2ban.local")


def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_yaml_file>")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    
    # check if SSH host keys exist
    if not check_ssh_host_keys():
        copy_ssh_default_config()
        generate_ssh_host_keys()
    
    # check if /config exists
    if not check_config():
        subprocess.run(
            ["cp", "/defaults/config/users.yaml", "/config/users.yaml"], check=True
        )
        print("Created /config/users.yaml .")
    
    # check if /etc/fail2ban/fail2ban.local exists
    if not check_fail2ban():
        shutil.copytree("/defaults/fail2ban/", "/etc/fail2ban/", dirs_exist_ok=True)
        print("Created /etc/fail2ban/jail.local .")
    
    # read YAML file and create users
    with open(yaml_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        users_list = data.get("users", [])
        unique_users_list = remove_duplicates(users_list)
        
        for user in unique_users_list:
            create_user(user["username"], user["userid"], user["sshkeys"])


if __name__ == "__main__":
    main()
    sys.exit(0)
