# Rancher Government - SUSE Manager

### These scripts are designed to help RGS setup support and package updates for your SUSE Manager instance.

## Instructions

Download the [suse_manager_info.sh](scripts/suse_manager_info.sh) and [last_update.py](scripts/last_update.py)

Once downloaded, modify the `last_update.py` and change the `MANAGER_PASSWORD` to match your SUMA Admin password, if you use a different login name other than `admin` then update the `MANAGER_LOGIN` as well.

Execute
```bash
zypper ref && zypper in -y spacewalk-utils* inter-server-sync
chmod +x suse_manager_info.sh && sh ./suse_manager_info.sh
```

Submit a ticket with the output of the `suma_info.txt`

## Data Gathered

These two scripts return the following information that will be critical in setting up support for your SUSE Manager under RGS.
1. SUSE Manager Version
     (retrieved via a zypper call)
2. List of Product Channels
     (retrieved via a `spacewalk-remove-channel -l`)
3. Last date the product channels were updated
     (this is retrieved from the last_update.py where it calls the API calls from SUSE Manager)

# *NO PRIVATE DATA IS RETRIEVED*
