#!/bin/bash

uname=$(uname -a)
name=$(echo $uname | cut -f2 -d" ")
ifconfig=$(ifconfig | grep -F "inet:" | grep -Fv "inet:127.0.0.1")
ip=$(echo $ifconfig | sed "s/.*inet:\([0-9]\{1,3\}\(\.[0-9]\{1,3\}\)\{3\}\).*/\1/")
uptime=$(top -b -n 1 | grep " up " | sed "s/.*up\( \)\{1,2\}\([0-9]\{1,2\}:[0-9][0-9]\).*/\2/")

echo "$name|$ip|$uptime|"
