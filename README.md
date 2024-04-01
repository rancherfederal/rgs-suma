# Rancher Government - SUSE Manager

## Why is this require?

As customers migrate from SUSE to RGS for their SUSE Manager will no longer be able to use Organizational Creditials from the SUSE Customer Center. To help with continued product selection and updates, there will be some engineering efforts to be made primarialy on RGS side but also some on the customers side of things. 

This doc is setup to help with that process. We are making every effor to make this as easy for you as the customer as possible.

In order for you to continue to receive updates for your SUSE Manager, RGS has to setup a SUSE Manger server to match your current product channels after which we will provide you with exports that you can import using `inter-server-sync`, this doc helps set up that process.

## Instructions

Download the [suma_info.py](scripts/suma_info.py)
### *This script is designed to help RGS setup support and package updates for your SUSE Manager instance.*

Once downloaded, modify the `suma_info.py` and change the `MANAGER_LOGIN` and `MANAGER_PASSWORD` as needed to match your SUMA Admin password.

Assuming you are still connected to the SUSE Customer Center (SCC), if you no longer have SCC access, another step will have to be done to allow you to execute the first command, so if you don't have SCC access, skip the first command and just run the script you downloaded.

Execute
```bash
zypper ref && zypper up && zypper in -y spacewalk-utils* inter-server-sync
chmod +x suma_info.py && python3 suma_info.py
```

Submit a ticket with the output of the `suma_info.txt`

## Data Gathered

This script returns the following information that will be critical in setting up support for your SUSE Manager under RGS.
1. SUSE Manager Version
2. List of Product Channels
3. Last date the product channels were updated
4. The last thing we need is your IP or IP Range, (we can also whitelist a set of CIDR) of your public IP address.

# *NO PRIVATE DATA IS RETRIEVED*
