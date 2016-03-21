#!/bin/bash

#PREFIX_ADDR="inet"
PREFIX_ADDR="inet adr"

uname=$(uname -a)
name=$(echo $uname | cut -f2 -d" ")
ifconfig=$(ifconfig | grep -F "$PREFIX_ADDR:" | grep -Fv "$PREFIX_ADDR:127.0.0.1")
ip=$(echo $ifconfig | sed "s/.*$PREFIX_ADDR:\([0-9]\{1,3\}\(\.[0-9]\{1,3\}\)\{3\}\).*/\1/")
uptime=$(top -b -n 1 | grep " up " | sed "s/.*up\( \)\{1,2\}\([0-9]\{1,2\}:[0-9][0-9]\).*/\2/")

echo "$name|$ip|$uptime|"
