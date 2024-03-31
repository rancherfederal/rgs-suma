#!/bin/bash

clist=$(spacewalk-remove-channel -l)
sumaver=$(zypper se -si notes | grep "release-notes-susemanager" | awk -F '|' '{print $4}' | xargs)
lastupdate="./last_update.py"

cat <<EOF > suma_info.txt
SUSE Manager Information

SUSE Manager version: $sumaver

List of Product Channels:
$(echo "${clist[@]}")

Last Update by channel:
$(python3 $lastupdate)
EOF
