#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script updates the Yaml file with the new SSH keys from the users .ssh directory
"""

import os
import subprocess
import yaml

def load_data_from_yaml():
    with open("/config/users.yaml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        return data


def sync_ssh_keys_with_yaml(user):
    
    
    ssh_dir = f"/home/{user['username']}/.ssh"
    authorized_keys_file = f"{ssh_dir}/authorized_keys"
    
    if os.path.exists(authorized_keys_file):
        with open(authorized_keys_file, "r") as file:
            user["sshkeys"] = file.readlines()
    else:
        user["sshkeys"] = []

def main():
    # read YAML file and create users
    with open("/config/users.yaml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        users_list = data.get("users", [])
        unique_users_list = remove_duplicates(users_list)
        create_user_list(unique_users_list)
    
    print("Updated Yaml file with new SSH keys.")