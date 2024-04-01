#!/usr/bin/python3
import re
import requests
import socket
from xmlrpc.client import ServerProxy, Error
import ssl

requests.packages.urllib3.disable_warnings()

SUMA_FQDN = socket.getfqdn()
MANAGER_LOGIN = "admin"
MANAGER_PASSWORD = "super_secret"
MANAGER_URL = "https://" + SUMA_FQDN

response = requests.get(MANAGER_URL, auth=(MANAGER_LOGIN, MANAGER_PASSWORD), verify=False)
version = "Unknown"
if response.status_code == 200:
    version_pattern = r"webVersion: '(\d+\.\d+\.\d+)'"
    match = re.search(version_pattern, response.text)
    if match:
        version = match.group(1)

context = ssl.create_default_context()
client = ServerProxy(f"{MANAGER_URL}/rpc/api", context=context)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

channel_list = client.channel.listVendorChannels(key)
channel_updates_info = []
for channel in channel_list:
    raw_date = client.channel.software.getChannelLastBuildById(key, channel["id"])
    formatted_date = raw_date.split()[0]
    channel_updates_info.append(f"{formatted_date} {channel['label']}")

client.auth.logout(key)

with open("suma_info.txt", "w") as file:
    file.write("SUSE Manager Information\n\n")
    file.write(f"SUSE Manager version: {version}\n\n")
    file.write("List of Product Channels:\n")
    file.write("\n".join([info.split()[1] for info in channel_updates_info]))
    file.write("\n\nProduct Channel Last Update:\n")
    file.write("\n".join(channel_updates_info))
