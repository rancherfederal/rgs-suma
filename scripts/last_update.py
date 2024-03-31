#! /usr/bin/python3

from xmlrpc.client import ServerProxy
import ssl
import socket

# Information needed to access and authenticate to SUSE Manager
SUMA_FQDN = socket.getfqdn()
MANAGER_LOGIN = "admin"
MANAGER_PASSWORD = "super_secret"

MANAGER_URL = "https://" + SUMA_FQDN + "/rpc/api"

# Connect and log in to SUSE Manager using SSL
context = ssl.create_default_context()
client = ServerProxy(MANAGER_URL, context=context)
key = client.auth.login(MANAGER_LOGIN, MANAGER_PASSWORD)

# Collect vendor channel build date
channel_list = client.channel.listVendorChannels(key)

for channel in channel_list:
    raw_date = client.channel.software.getChannelLastBuildById(key, channel["id"])
    print(raw_date.split()[0] + " " + channel["label"])
