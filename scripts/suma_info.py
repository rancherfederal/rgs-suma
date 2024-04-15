#!/usr/bin/python3

import os
import re
import requests
import socket
import ssl
import configparser
from xmlrpc.client import ServerProxy

# Disable SSL warnings due to verify=False
requests.packages.urllib3.disable_warnings()

# Function to create the XML-RPC client and login
def create_client():
    config_path = os.path.expanduser('/root/.mgr-sync')
    config = configparser.ConfigParser()
    with open(config_path, 'r') as f:
         config.read_string('[DEFAULT]\n' + f.read())    # work around since the mgr-sync does not have headers
    MANAGER_LOGIN = config.get('DEFAULT', 'mgrsync.user')
    MANAGER_PASSWORD = config.get('DEFAULT', 'mgrsync.password')
    SUMA_FQDN = socket.getfqdn()
    MANAGER_URL = f"https://{SUMA_FQDN}/rpc/api"
    context = ssl.create_default_context()
    client = ServerProxy(MANAGER_URL, context=context)
    key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)
    return client, key, MANAGER_URL

# Get the client, session key, and URL from create_client
client, key, MANAGER_URL = create_client()

# Fetch the SUSE Manager version using requests
response = requests.get(MANAGER_URL.replace("/rpc/api", ""), verify=False)
version = "Unknown"
if response.status_code == 200:
    version_pattern = r"webVersion: '(\d+\.\d+\.\d+)'"
    match = re.search(version_pattern, response.text)
    if match:
        version = match.group(1)

# Fetch channel updates info
channel_list = client.channel.listVendorChannels(key)
channel_updates_info = []
for channel in channel_list:
    raw_date = client.channel.software.getChannelLastBuildById(key, channel["id"])
    formatted_date = raw_date.split()[0]
    channel_updates_info.append(f"{formatted_date} {channel['label']}")

# Log out after operations
client.auth.logout(key)

# Write information to a file
with open("suma_info.txt", "w") as file:
    file.write("SUSE Manager Information\n\n")
    file.write(f"SUSE Manager version: {version}\n\n")
    file.write("List of Product Channels:\n")
    file.write("\n".join([info.split()[1] for info in channel_updates_info]))
    file.write("\n\nProduct Channel Last Update:\n")
    file.write("\n".join(channel_updates_info))
